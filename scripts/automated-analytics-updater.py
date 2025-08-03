#!/usr/bin/env python3
"""
Automated GitHub Analytics Updater
Real-time data collection with interactive visualizations and mobile responsiveness
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import asyncio
import aiohttp
from dataclasses import dataclass, asdict
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class RepositoryMetrics:
    name: str
    stars: int
    forks: int
    issues: int
    prs: int
    size: int
    language: str
    last_updated: str
    contributors: int
    commits_30d: int
    health_score: float

@dataclass
class LanguageStats:
    name: str
    bytes: int
    percentage: float
    repos: int
    lines_of_code: int

@dataclass
class ActivityMetrics:
    commits_today: int
    commits_week: int
    commits_month: int
    prs_opened: int
    prs_merged: int
    issues_opened: int
    issues_closed: int
    streak_days: int

class GitHubAnalyticsCollector:
    def __init__(self, username: str, token: Optional[str] = None):
        self.username = username
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': f'github-analytics-collector/{username}'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = time.time()
        
    async def make_request(self, session: aiohttp.ClientSession, url: str, params: Dict = None) -> Optional[Dict]:
        """Make async API request with rate limiting"""
        if self.rate_limit_remaining <= 10:
            wait_time = max(0, self.rate_limit_reset - time.time())
            if wait_time > 0:
                logger.info(f"Rate limit low, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
        
        try:
            async with session.get(url, params=params, headers=self.headers) as response:
                # Update rate limit info
                self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
                self.rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', time.time()))
                
                if response.status == 200:
                    return await response.json()
                elif response.status == 403:
                    logger.warning(f"Rate limit hit: {response.status}")
                    await asyncio.sleep(60)
                    return await self.make_request(session, url, params)
                else:
                    logger.error(f"API request failed: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None
    
    async def collect_user_data(self, session: aiohttp.ClientSession) -> Dict:
        """Collect basic user information"""
        url = f"{self.base_url}/users/{self.username}"
        return await self.make_request(session, url) or {}
    
    async def collect_repositories(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Collect all repositories with detailed metrics"""
        repos = []
        page = 1
        
        while True:
            url = f"{self.base_url}/users/{self.username}/repos"
            params = {'page': page, 'per_page': 100, 'sort': 'updated', 'direction': 'desc'}
            
            data = await self.make_request(session, url, params)
            if not data:
                break
            
            repos.extend(data)
            if len(data) < 100:
                break
            page += 1
        
        # Collect detailed metrics for each repo
        detailed_repos = []
        for repo in repos:
            detailed_repo = await self.collect_repository_details(session, repo)
            if detailed_repo:
                detailed_repos.append(detailed_repo)
        
        return detailed_repos
    
    async def collect_repository_details(self, session: aiohttp.ClientSession, repo: Dict) -> Optional[RepositoryMetrics]:
        """Collect detailed repository metrics"""
        repo_name = repo['name']
        
        # Collect languages
        languages_url = f"{self.base_url}/repos/{self.username}/{repo_name}/languages"
        languages = await self.make_request(session, languages_url) or {}
        
        # Collect contributors
        contributors_url = f"{self.base_url}/repos/{self.username}/{repo_name}/contributors"
        contributors = await self.make_request(session, contributors_url) or []
        
        # Collect recent commits (last 30 days)
        since_date = (datetime.now() - timedelta(days=30)).isoformat()
        commits_url = f"{self.base_url}/repos/{self.username}/{repo_name}/commits"
        commits = await self.make_request(session, commits_url, {'since': since_date, 'per_page': 100}) or []
        
        # Calculate health score
        health_score = self.calculate_repo_health_score(repo, languages, contributors, commits)
        
        return RepositoryMetrics(
            name=repo_name,
            stars=repo.get('stargazers_count', 0),
            forks=repo.get('forks_count', 0),
            issues=repo.get('open_issues_count', 0),
            prs=0,  # Will be calculated separately
            size=repo.get('size', 0),
            language=repo.get('language', 'Unknown'),
            last_updated=repo.get('updated_at', ''),
            contributors=len(contributors),
            commits_30d=len(commits),
            health_score=health_score
        )
    
    def calculate_repo_health_score(self, repo: Dict, languages: Dict, contributors: List, commits: List) -> float:
        """Calculate repository health score (0-100)"""
        score = 0
        
        # Activity score (40 points)
        if commits:
            score += min(40, len(commits) * 2)
        
        # Community score (30 points)
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        score += min(20, stars * 0.5)
        score += min(10, forks * 1)
        
        # Maintenance score (30 points)
        updated_at = datetime.fromisoformat(repo.get('updated_at', '').replace('Z', '+00:00'))
        days_since_update = (datetime.now() - updated_at.replace(tzinfo=None)).days
        
        if days_since_update <= 7:
            score += 30
        elif days_since_update <= 30:
            score += 20
        elif days_since_update <= 90:
            score += 10
        
        return min(100, score)
    
    async def collect_activity_metrics(self, session: aiohttp.ClientSession) -> ActivityMetrics:
        """Collect user activity metrics"""
        events_url = f"{self.base_url}/users/{self.username}/events"
        events = await self.make_request(session, events_url, {'per_page': 100}) or []
        
        now = datetime.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        commits_today = 0
        commits_week = 0
        commits_month = 0
        prs_opened = 0
        prs_merged = 0
        issues_opened = 0
        issues_closed = 0
        
        for event in events:
            event_date = datetime.fromisoformat(event['created_at'].replace('Z', '+00:00')).replace(tzinfo=None)
            event_type = event.get('type', '')
            
            if event_type == 'PushEvent':
                commits = len(event.get('payload', {}).get('commits', []))
                if event_date.date() == today:
                    commits_today += commits
                if event_date >= week_ago:
                    commits_week += commits
                if event_date >= month_ago:
                    commits_month += commits
            
            elif event_type == 'PullRequestEvent':
                action = event.get('payload', {}).get('action', '')
                if action == 'opened' and event_date >= month_ago:
                    prs_opened += 1
                elif action == 'closed' and event_date >= month_ago:
                    prs_merged += 1
            
            elif event_type == 'IssuesEvent':
                action = event.get('payload', {}).get('action', '')
                if action == 'opened' and event_date >= month_ago:
                    issues_opened += 1
                elif action == 'closed' and event_date >= month_ago:
                    issues_closed += 1
        
        # Calculate streak (simplified)
        streak_days = self.calculate_commit_streak(events)
        
        return ActivityMetrics(
            commits_today=commits_today,
            commits_week=commits_week,
            commits_month=commits_month,
            prs_opened=prs_opened,
            prs_merged=prs_merged,
            issues_opened=issues_opened,
            issues_closed=issues_closed,
            streak_days=streak_days
        )
    
    def calculate_commit_streak(self, events: List[Dict]) -> int:
        """Calculate current commit streak"""
        commit_dates = set()
        
        for event in events:
            if event.get('type') == 'PushEvent':
                event_date = datetime.fromisoformat(event['created_at'].replace('Z', '+00:00')).date()
                commit_dates.add(event_date)
        
        if not commit_dates:
            return 0
        
        sorted_dates = sorted(commit_dates, reverse=True)
        streak = 0
        current_date = datetime.now().date()
        
        for date in sorted_dates:
            if date == current_date or date == current_date - timedelta(days=1):
                streak += 1
                current_date = date - timedelta(days=1)
            else:
                break
        
        return streak
    
    async def collect_all_analytics(self) -> Dict:
        """Collect all analytics data"""
        logger.info("Starting comprehensive analytics collection...")
        
        async with aiohttp.ClientSession() as session:
            # Collect all data concurrently
            user_data_task = self.collect_user_data(session)
            repos_task = self.collect_repositories(session)
            activity_task = self.collect_activity_metrics(session)
            
            user_data, repos, activity = await asyncio.gather(
                user_data_task, repos_task, activity_task
            )
        
        # Process language statistics
        language_stats = self.process_language_stats(repos)
        
        # Calculate summary metrics
        summary_metrics = self.calculate_summary_metrics(repos, activity)
        
        analytics_data = {
            'timestamp': datetime.now().isoformat(),
            'user_data': user_data,
            'repositories': [asdict(repo) for repo in repos],
            'language_stats': [asdict(lang) for lang in language_stats],
            'activity_metrics': asdict(activity),
            'summary_metrics': summary_metrics,
            'collection_info': {
                'total_repos': len(repos),
                'rate_limit_remaining': self.rate_limit_remaining,
                'collection_duration': time.time()
            }
        }
        
        return analytics_data
    
    def process_language_stats(self, repos: List[RepositoryMetrics]) -> List[LanguageStats]:
        """Process language statistics from repositories"""
        language_data = {}
        
        for repo in repos:
            if repo.language and repo.language != 'Unknown':
                if repo.language not in language_data:
                    language_data[repo.language] = {
                        'bytes': 0,
                        'repos': 0,
                        'lines_estimate': 0
                    }
                
                language_data[repo.language]['bytes'] += repo.size * 1024  # Convert KB to bytes
                language_data[repo.language]['repos'] += 1
                language_data[repo.language]['lines_estimate'] += repo.size * 20  # Rough estimate
        
        total_bytes = sum(data['bytes'] for data in language_data.values())
        
        language_stats = []
        for lang, data in language_data.items():
            percentage = (data['bytes'] / total_bytes * 100) if total_bytes > 0 else 0
            language_stats.append(LanguageStats(
                name=lang,
                bytes=data['bytes'],
                percentage=percentage,
                repos=data['repos'],
                lines_of_code=data['lines_estimate']
            ))
        
        return sorted(language_stats, key=lambda x: x.percentage, reverse=True)
    
    def calculate_summary_metrics(self, repos: List[RepositoryMetrics], activity: ActivityMetrics) -> Dict:
        """Calculate summary metrics"""
        total_stars = sum(repo.stars for repo in repos)
        total_forks = sum(repo.forks for repo in repos)
        avg_health_score = sum(repo.health_score for repo in repos) / len(repos) if repos else 0
        
        active_repos = len([repo for repo in repos if repo.commits_30d > 0])
        top_repo = max(repos, key=lambda x: x.stars) if repos else None
        
        return {
            'total_repositories': len(repos),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'average_health_score': round(avg_health_score, 1),
            'active_repositories': active_repos,
            'top_repository': {
                'name': top_repo.name if top_repo else '',
                'stars': top_repo.stars if top_repo else 0
            },
            'productivity_score': self.calculate_productivity_score(activity),
            'community_engagement': total_stars + total_forks
        }
    
    def calculate_productivity_score(self, activity: ActivityMetrics) -> float:
        """Calculate productivity score based on activity"""
        score = 0
        score += activity.commits_month * 2
        score += activity.prs_opened * 5
        score += activity.prs_merged * 8
        score += activity.issues_closed * 3
        score += activity.streak_days * 1
        
        return min(100, score)

async def main():
    """Main execution function"""
    username = os.getenv('GITHUB_USERNAME', 'Xenonesis')
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        logger.warning("No GitHub token provided. API requests will be limited.")
    
    collector = GitHubAnalyticsCollector(username, token)
    
    try:
        analytics_data = await collector.collect_all_analytics()
        
        # Save analytics data
        with open('analytics-data.json', 'w') as f:
            json.dump(analytics_data, f, indent=2, default=str)
        
        logger.info(f"Analytics collection completed successfully!")
        logger.info(f"Collected data for {analytics_data['collection_info']['total_repos']} repositories")
        logger.info(f"Rate limit remaining: {analytics_data['collection_info']['rate_limit_remaining']}")
        
        return analytics_data
        
    except Exception as e:
        logger.error(f"Error collecting analytics: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())