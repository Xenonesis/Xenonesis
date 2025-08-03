#!/usr/bin/env python3
"""
GitHub Analytics Runner
Main entry point for running all analytics components
"""

import os
import sys
import asyncio
import argparse
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup required directories and environment"""
    directories = ['backups', 'config', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

async def run_data_collection():
    """Run analytics data collection"""
    logger.info("Starting analytics data collection...")
    
    try:
        # Import and run the analytics collector
        sys.path.append('scripts')
        from automated_analytics_updater import GitHubAnalyticsCollector
        
        username = os.getenv('GITHUB_USERNAME') or os.getenv('GH_USERNAME', 'Xenonesis')
        token = os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
        
        if not token:
            logger.warning("No GitHub token found. API requests will be limited.")
        
        collector = GitHubAnalyticsCollector(username, token)
        analytics_data = await collector.collect_all_analytics()
        
        # Save the data
        with open('analytics-data.json', 'w') as f:
            json.dump(analytics_data, f, indent=2, default=str)
        
        logger.info(f"Data collection completed. Processed {analytics_data['collection_info']['total_repos']} repositories")
        return analytics_data
        
    except Exception as e:
        logger.error(f"Data collection failed: {e}")
        raise

def generate_dashboards(analytics_data):
    """Generate all dashboard variants"""
    logger.info("Generating dashboards...")
    
    try:
        # Import dashboard generators
        sys.path.append('scripts')
        from interactive_dashboard_generator import InteractiveDashboardGenerator
        from mobile_responsive_updater import MobileResponsiveUpdater
        
        # Generate interactive dashboard
        interactive_generator = InteractiveDashboardGenerator(analytics_data)
        interactive_html = interactive_generator.generate_dashboard()
        
        with open('interactive-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(interactive_html)
        logger.info("Interactive dashboard generated successfully")
        
        # Generate mobile dashboard
        mobile_generator = MobileResponsiveUpdater(analytics_data)
        mobile_html = mobile_generator.generate_mobile_optimized_html()
        
        with open('mobile-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(mobile_html)
        logger.info("Mobile dashboard generated successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Dashboard generation failed: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

def update_readme_and_analytics(analytics_data):
    """Update README and analytics markdown files"""
    logger.info("Updating README and analytics files...")
    
    try:
        # Update README badges
        update_readme_badges(analytics_data)
        
        # Update analytics markdown
        update_analytics_markdown(analytics_data)
        
        logger.info("README and analytics files updated")
        return True
        
    except Exception as e:
        logger.error(f"README/analytics update failed: {e}")
        return False

def update_readme_badges(analytics_data):
    """Update badges in README.md"""
    import re
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        summary = analytics_data.get('summary_metrics', {})
        activity = analytics_data.get('activity_metrics', {})
        
        # Define badge updates
        updates = {
            'Total%20Repositories': str(summary.get('total_repositories', 0)),
            'Total%20Stars': str(summary.get('total_stars', 0)),
            'Active%20Repos': str(summary.get('active_repositories', 0)),
            'Health%20Score': f"{summary.get('average_health_score', 0):.1f}%25",
            'Commits%20This%20Month': str(activity.get('commits_month', 0)),
            'Current%20Streak': f"{activity.get('streak_days', 0)}%20days"
        }
        
        # Apply updates
        for key, value in updates.items():
            pattern = f'(https://img\\.shields\\.io/badge/{key.replace("%20", "%20")}-)[^-]+(-.+?(?:alt=|"))'
            replacement = f'\\g<1>{value}\\g<2>'
            content = re.sub(pattern, replacement, content)
        
        # Update language percentages
        languages = analytics_data.get('language_stats', [])
        if languages:
            for i, lang in enumerate(languages[:4]):
                lang_name = lang.get('name', '').replace('+', '%2B')
                percentage = lang.get('percentage', 0)
                
                # Update specific language badges
                if lang_name == 'Python':
                    content = re.sub(
                        r'(https://img\.shields\.io/badge/)\d+\.\d+(%25-Usage-blue)',
                        f'\\g<1>{percentage:.1f}\\g<2>',
                        content
                    )
                elif lang_name == 'JavaScript':
                    content = re.sub(
                        r'(https://img\.shields\.io/badge/)\d+\.\d+(%25-Usage-yellow)',
                        f'\\g<1>{percentage:.1f}\\g<2>',
                        content
                    )
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        logger.error(f"Error updating README badges: {e}")
        raise

def update_analytics_markdown(analytics_data):
    """Update repository-analytics.md with detailed data"""
    try:
        summary = analytics_data.get('summary_metrics', {})
        repos = analytics_data.get('repositories', [])
        languages = analytics_data.get('language_stats', [])
        activity = analytics_data.get('activity_metrics', {})
        
        # Generate top repositories table
        top_repos = sorted(repos, key=lambda x: x.get('stars', 0), reverse=True)[:10]
        
        repo_table = "| Repository | Stars | Forks | Issues | Language | Health Score | Last Updated |\n"
        repo_table += "|------------|-------|-------|--------|----------|--------------|-------------|\n"
        
        for repo in top_repos:
            last_updated = datetime.fromisoformat(repo.get('last_updated', '').replace('Z', '+00:00'))
            days_ago = (datetime.now() - last_updated.replace(tzinfo=None)).days
            
            repo_table += f"| {repo.get('name', 'Unknown')} | ⭐ {repo.get('stars', 0)} | 🍴 {repo.get('forks', 0)} | 🐛 {repo.get('issues', 0)} | {repo.get('language', 'Unknown')} | {repo.get('health_score', 0):.1f}% | {days_ago} days ago |\n"
        
        # Generate language stats
        lang_stats = ""
        for lang in languages[:10]:
            lang_stats += f"- **{lang.get('name', 'Unknown')}**: {lang.get('percentage', 0):.1f}% ({lang.get('repos', 0)} repos)\n"
        
        # Create updated analytics content
        analytics_content = f"""# 📊 Advanced Repository Analytics & Language Insights

*Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*

## 🏆 Repository Performance Metrics

### Summary Statistics
- **Total Repositories**: {summary.get('total_repositories', 0)}
- **Total Stars**: {summary.get('total_stars', 0)}
- **Total Forks**: {summary.get('total_forks', 0)}
- **Average Health Score**: {summary.get('average_health_score', 0):.1f}%
- **Active Repositories**: {summary.get('active_repositories', 0)}
- **Community Engagement**: {summary.get('community_engagement', 0)}

### Top Performing Repositories
{repo_table}

## 💻 Language Usage Deep Dive

### Primary Languages by Usage
{lang_stats}

## 🚀 Development Activity Metrics

### Recent Activity Summary
- **Commits Today**: {activity.get('commits_today', 0)}
- **Commits This Week**: {activity.get('commits_week', 0)}
- **Commits This Month**: {activity.get('commits_month', 0)}
- **Pull Requests Opened**: {activity.get('prs_opened', 0)}
- **Pull Requests Merged**: {activity.get('prs_merged', 0)}
- **Issues Opened**: {activity.get('issues_opened', 0)}
- **Issues Closed**: {activity.get('issues_closed', 0)}
- **Current Streak**: {activity.get('streak_days', 0)} days

## 📈 Performance Analytics

### Repository Health Distribution
```
Excellent (90-100%): {len([r for r in repos if r.get('health_score', 0) >= 90])} repositories
Good (70-89%):       {len([r for r in repos if 70 <= r.get('health_score', 0) < 90])} repositories
Fair (50-69%):       {len([r for r in repos if 50 <= r.get('health_score', 0) < 70])} repositories
Needs Attention:     {len([r for r in repos if r.get('health_score', 0) < 50])} repositories
```

### Productivity Metrics
- **Productivity Score**: {summary.get('productivity_score', 0):.1f}/100
- **Average Repository Size**: {sum(r.get('size', 0) for r in repos) / len(repos) / 1024:.1f} MB
- **Most Active Repository**: {max(repos, key=lambda x: x.get('commits_30d', 0)).get('name', 'N/A') if repos else 'N/A'}

## 🔗 Interactive Dashboards

- **[📱 Mobile Dashboard](./mobile-dashboard.html)** - Optimized for mobile devices
- **[💻 Interactive Dashboard](./interactive-dashboard.html)** - Full-featured desktop experience

---

*This report is automatically generated from GitHub API data.*
*For real-time updates, the system refreshes every 6 hours.*

### Key Features
• **Real Data Integration** - All metrics pull from actual GitHub APIs
• **Professional Presentation** - Organized tables and structured layouts  
• **Comprehensive Coverage** - From basic stats to advanced analytics
• **Visual Appeal** - Consistent Tokyo Night theme with modern badges
• **Actionable Insights** - Performance benchmarks and improvement areas
• **Community Focus** - Collaboration and contribution metrics
• **Mobile Responsive** - Optimized viewing on all devices
• **Interactive Visualizations** - Charts and graphs for better understanding
"""
        
        with open('repository-analytics.md', 'w', encoding='utf-8') as f:
            f.write(analytics_content)
            
    except Exception as e:
        logger.error(f"Error updating analytics markdown: {e}")
        raise

async def run_current_activities_update():
    """Update Current Activities section with real GitHub data"""
    logger.info("Updating Current Activities section...")
    
    try:
        # Import and run the current activities updater
        sys.path.append('scripts')
        from current_activities_updater import CurrentActivitiesUpdater
        
        username = os.getenv('GITHUB_USERNAME') or os.getenv('GH_USERNAME', 'Xenonesis')
        token = os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
        
        updater = CurrentActivitiesUpdater(username, token)
        success = await updater.update_readme_current_activities()
        
        logger.info(f"Current Activities update: {'✅' if success else '❌'}")
        return success
        
    except Exception as e:
        logger.error(f"Current Activities update failed: {e}")
        return False

async def run_full_pipeline():
    """Run the complete analytics pipeline"""
    start_time = datetime.now()
    logger.info("Starting complete GitHub analytics pipeline...")
    
    try:
        # Setup environment
        setup_environment()
        
        # Step 1: Collect analytics data
        analytics_data = await run_data_collection()
        
        # Step 2: Generate dashboards
        dashboard_success = generate_dashboards(analytics_data)
        
        # Step 3: Update README and analytics
        readme_success = update_readme_and_analytics(analytics_data)
        
        # Step 4: Update Current Activities with real-time data
        activities_success = await run_current_activities_update()
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Summary
        logger.info("="*60)
        logger.info("GITHUB ANALYTICS PIPELINE COMPLETED")
        logger.info("="*60)
        logger.info(f"Execution Time: {execution_time:.2f} seconds")
        logger.info(f"Repositories Processed: {analytics_data['collection_info']['total_repos']}")
        logger.info(f"Interactive Dashboard: {'✅' if dashboard_success else '❌'}")
        logger.info(f"Mobile Dashboard: {'✅' if dashboard_success else '❌'}")
        logger.info(f"README Updated: {'✅' if readme_success else '❌'}")
        logger.info(f"Analytics Updated: {'✅' if readme_success else '❌'}")
        logger.info(f"Current Activities: {'✅' if activities_success else '❌'}")
        logger.info(f"Rate Limit Remaining: {analytics_data['collection_info']['rate_limit_remaining']}")
        logger.info("="*60)
        
        # Create summary file
        summary = {
            'timestamp': datetime.now().isoformat(),
            'execution_time_seconds': execution_time,
            'repositories_processed': analytics_data['collection_info']['total_repos'],
            'dashboards_generated': dashboard_success,
            'readme_updated': readme_success,
            'current_activities_updated': activities_success,
            'rate_limit_remaining': analytics_data['collection_info']['rate_limit_remaining'],
            'total_stars': analytics_data['summary_metrics']['total_stars'],
            'total_repositories': analytics_data['summary_metrics']['total_repositories'],
            'health_score': analytics_data['summary_metrics']['average_health_score']
        }
        
        with open('pipeline-summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        return True
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return False

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='GitHub Analytics Pipeline')
    parser.add_argument('--collect-only', action='store_true', 
                       help='Only collect data, skip dashboard generation')
    parser.add_argument('--dashboards-only', action='store_true',
                       help='Only generate dashboards from existing data')
    parser.add_argument('--update-only', action='store_true',
                       help='Only update README and analytics files')
    parser.add_argument('--activities-only', action='store_true',
                       help='Only update Current Activities section')
    parser.add_argument('--setup', action='store_true',
                       help='Setup environment and create config files')
    
    args = parser.parse_args()
    
    if args.setup:
        logger.info("Setting up GitHub Analytics environment...")
        setup_environment()
        
        # Create sample config
        config_content = """# GitHub Analytics Configuration
# Set your GitHub username and token as environment variables:
# export GITHUB_USERNAME="your-username"
# export GITHUB_TOKEN="your-personal-access-token"

# Optional: Email notifications
# export SMTP_SERVER="smtp.gmail.com"
# export SMTP_PORT="587"
# export EMAIL_USER="your-email@gmail.com"
# export EMAIL_PASS="your-app-password"
# export NOTIFICATION_EMAIL="notifications@example.com"
"""
        
        with open('config/setup.md', 'w') as f:
            f.write(config_content)
        
        logger.info("Setup completed! Check config/setup.md for configuration instructions.")
        return
    
    if args.collect_only:
        logger.info("Running data collection only...")
        asyncio.run(run_data_collection())
        
    elif args.dashboards_only:
        logger.info("Generating dashboards only...")
        try:
            with open('analytics-data.json', 'r') as f:
                analytics_data = json.load(f)
            generate_dashboards(analytics_data)
        except FileNotFoundError:
            logger.error("No analytics data found. Run data collection first.")
            
    elif args.update_only:
        logger.info("Updating README and analytics only...")
        try:
            with open('analytics-data.json', 'r') as f:
                analytics_data = json.load(f)
            update_readme_and_analytics(analytics_data)
        except FileNotFoundError:
            logger.error("No analytics data found. Run data collection first.")
    
    elif args.activities_only:
        logger.info("Updating Current Activities only...")
        asyncio.run(run_current_activities_update())
            
    else:
        # Run full pipeline
        success = asyncio.run(run_full_pipeline())
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()