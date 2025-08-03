#!/usr/bin/env python3
"""
GitHub Statistics Auto-Update Script
Automatically fetches and updates GitHub statistics in README.md
"""

import os
import re
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import base64

class GitHubStatsUpdater:
    def __init__(self, username: str, token: str = None):
        self.username = username
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.token}' if self.token else {},
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
        
    def fetch_user_data(self) -> Dict[str, Any]:
        """Fetch basic user information"""
        response = requests.get(f'{self.base_url}/users/{self.username}', headers=self.headers)
        return response.json() if response.status_code == 200 else {}
    
    def fetch_repositories(self) -> List[Dict[str, Any]]:
        """Fetch all repositories for the user"""
        repos = []
        page = 1
        while True:
            response = requests.get(
                f'{self.base_url}/users/{self.username}/repos',
                headers=self.headers,
                params={'page': page, 'per_page': 100, 'sort': 'updated'}
            )
            if response.status_code != 200:
                break
            
            page_repos = response.json()
            if not page_repos:
                break
                
            repos.extend(page_repos)
            page += 1
            
        return repos
    
    def fetch_repository_stats(self, repo_name: str) -> Dict[str, Any]:
        """Fetch detailed statistics for a specific repository"""
        stats = {}
        
        # Basic repo info
        repo_response = requests.get(f'{self.base_url}/repos/{self.username}/{repo_name}', headers=self.headers)
        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            stats.update({
                'stars': repo_data.get('stargazers_count', 0),
                'forks': repo_data.get('forks_count', 0),
                'size': repo_data.get('size', 0),
                'language': repo_data.get('language', 'Unknown'),
                'updated_at': repo_data.get('updated_at', ''),
                'created_at': repo_data.get('created_at', ''),
                'open_issues': repo_data.get('open_issues_count', 0)
            })
        
        # Languages
        lang_response = requests.get(f'{self.base_url}/repos/{self.username}/{repo_name}/languages', headers=self.headers)
        if lang_response.status_code == 200:
            stats['languages'] = lang_response.json()
        
        # Contributors
        contrib_response = requests.get(f'{self.base_url}/repos/{self.username}/{repo_name}/contributors', headers=self.headers)
        if contrib_response.status_code == 200:
            stats['contributors_count'] = len(contrib_response.json())
        
        # Recent commits (last 30 days)
        since_date = (datetime.now() - timedelta(days=30)).isoformat()
        commits_response = requests.get(
            f'{self.base_url}/repos/{self.username}/{repo_name}/commits',
            headers=self.headers,
            params={'since': since_date, 'per_page': 100}
        )
        if commits_response.status_code == 200:
            stats['recent_commits'] = len(commits_response.json())
        
        return stats
    
    def calculate_language_stats(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate language usage statistics"""
        language_bytes = {}
        language_repos = {}
        
        for repo in repos:
            if repo.get('fork'):  # Skip forked repositories
                continue
                
            repo_stats = self.fetch_repository_stats(repo['name'])
            languages = repo_stats.get('languages', {})
            
            for lang, bytes_count in languages.items():
                language_bytes[lang] = language_bytes.get(lang, 0) + bytes_count
                language_repos[lang] = language_repos.get(lang, 0) + 1
        
        total_bytes = sum(language_bytes.values())
        
        return {
            'by_bytes': {lang: (bytes_count / total_bytes * 100) for lang, bytes_count in language_bytes.items()},
            'by_repos': language_repos,
            'total_bytes': total_bytes
        }
    
    def calculate_repository_metrics(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate repository health and activity metrics"""
        total_repos = len(repos)
        public_repos = len([r for r in repos if not r.get('private', True)])
        forked_repos = len([r for r in repos if r.get('fork', False)])
        original_repos = total_repos - forked_repos
        
        # Calculate sizes
        total_size = sum(r.get('size', 0) for r in repos)
        avg_size = total_size / total_repos if total_repos > 0 else 0
        
        # Activity metrics
        now = datetime.now()
        active_repos = 0
        recently_updated = 0
        
        for repo in repos:
            updated_at = datetime.fromisoformat(repo.get('updated_at', '').replace('Z', '+00:00'))
            days_since_update = (now - updated_at.replace(tzinfo=None)).days
            
            if days_since_update <= 30:
                active_repos += 1
            if days_since_update <= 7:
                recently_updated += 1
        
        stale_repos = total_repos - active_repos
        
        return {
            'total_repos': total_repos,
            'public_repos': public_repos,
            'forked_repos': forked_repos,
            'original_repos': original_repos,
            'total_size_mb': round(total_size / 1024, 1),
            'avg_size_mb': round(avg_size / 1024, 1),
            'active_repos': active_repos,
            'stale_repos': stale_repos,
            'recently_updated': recently_updated
        }
    
    def get_top_repositories(self, repos: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Get top repositories by stars"""
        non_fork_repos = [r for r in repos if not r.get('fork', False)]
        sorted_repos = sorted(non_fork_repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)
        
        top_repos = []
        for repo in sorted_repos[:limit]:
            repo_stats = self.fetch_repository_stats(repo['name'])
            top_repos.append({
                'name': repo['name'],
                'description': repo.get('description', ''),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'language': repo.get('language', 'Unknown'),
                'updated_at': repo.get('updated_at', ''),
                'open_issues': repo.get('open_issues_count', 0),
                'recent_commits': repo_stats.get('recent_commits', 0)
            })
        
        return top_repos
    
    def update_readme_stats(self, readme_path: str = 'README.md'):
        """Update statistics in README.md file"""
        print("🚀 Starting GitHub statistics update...")
        
        # Fetch data
        user_data = self.fetch_user_data()
        repos = self.fetch_repositories()
        language_stats = self.calculate_language_stats(repos)
        repo_metrics = self.calculate_repository_metrics(repos)
        top_repos = self.get_top_repositories(repos)
        
        # Read current README
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update statistics
        updates = {
            'Total%20Repositories': str(repo_metrics['total_repos']),
            'Public%20Repos': str(repo_metrics['public_repos']),
            'Forked%20Repos': str(repo_metrics['forked_repos']),
            'Original%20Repos': str(repo_metrics['original_repos']),
            'Total%20Size': f"{repo_metrics['total_size_mb']}MB",
            'Avg%20Repo%20Size': f"{repo_metrics['avg_size_mb']}MB",
            'Active%20Repos': str(repo_metrics['active_repos']),
            'Stale%20Repos': str(repo_metrics['stale_repos']),
            'Recently%20Updated': str(repo_metrics['recently_updated'])
        }
        
        # Apply updates to README
        for key, value in updates.items():
            pattern = f'(https://img\\.shields\\.io/badge/{key}-)[^-]+(-.+?alt=)'
            replacement = f'\\g<1>{value}\\g<2>'
            content = re.sub(pattern, replacement, content)
        
        # Update language percentages
        top_languages = sorted(language_stats['by_bytes'].items(), key=lambda x: x[1], reverse=True)[:4]
        for i, (lang, percentage) in enumerate(top_languages):
            pattern = f'(https://img\\.shields\\.io/badge/{percentage:.1f}%25-Usage-)'
            if lang == 'Python':
                content = re.sub(r'(https://img\.shields\.io/badge/)\d+\.\d+(%25-Usage-blue)', f'\\g<1>{percentage:.1f}\\g<2>', content)
            elif lang == 'JavaScript':
                content = re.sub(r'(https://img\.shields\.io/badge/)\d+\.\d+(%25-Usage-yellow)', f'\\g<1>{percentage:.1f}\\g<2>', content)
        
        # Write updated README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Generate analytics report
        self.generate_analytics_report(user_data, repos, language_stats, repo_metrics, top_repos)
        
        print("✅ GitHub statistics updated successfully!")
        print(f"📊 Processed {len(repos)} repositories")
        print(f"🏆 Top repository: {top_repos[0]['name'] if top_repos else 'None'} ({top_repos[0]['stars'] if top_repos else 0} stars)")
    
    def generate_analytics_report(self, user_data, repos, language_stats, repo_metrics, top_repos):
        """Generate detailed analytics report"""
        report = f"""# 📊 GitHub Analytics Report
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 📈 Repository Overview
- **Total Repositories**: {repo_metrics['total_repos']}
- **Public Repositories**: {repo_metrics['public_repos']}
- **Original Repositories**: {repo_metrics['original_repos']}
- **Total Size**: {repo_metrics['total_size_mb']} MB
- **Active Repositories**: {repo_metrics['active_repos']}

## 🏆 Top Repositories
"""
        
        for i, repo in enumerate(top_repos[:5], 1):
            report += f"{i}. **{repo['name']}** - ⭐ {repo['stars']} stars, 🍴 {repo['forks']} forks ({repo['language']})\n"
        
        report += "\n## 💻 Language Distribution\n"
        for lang, percentage in sorted(language_stats['by_bytes'].items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"- **{lang}**: {percentage:.1f}%\n"
        
        with open('repository-analytics-auto.md', 'w', encoding='utf-8') as f:
            f.write(report)

def main():
    """Main execution function"""
    username = os.getenv('GITHUB_USERNAME', 'Xenonesis')
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("⚠️  Warning: GITHUB_TOKEN not found. API rate limits may apply.")
    
    updater = GitHubStatsUpdater(username, token)
    updater.update_readme_stats()

if __name__ == "__main__":
    main()