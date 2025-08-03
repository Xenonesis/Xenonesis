#!/usr/bin/env python3
"""
Interactive Dashboard Generator
Creates mobile-responsive HTML dashboard with interactive visualizations
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class InteractiveDashboardGenerator:
    def __init__(self, analytics_data: Dict):
        self.data = analytics_data
        self.timestamp = analytics_data.get('timestamp', datetime.now().isoformat())
        
    def generate_dashboard(self) -> str:
        """Generate complete interactive dashboard HTML"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Analytics Dashboard - {self.data.get('user_data', {}).get('login', 'User')}</title>
    
    <!-- External Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        {self.generate_css()}
    </style>
</head>
<body>
    <div class="dashboard-container">
        {self.generate_header()}
        {self.generate_summary_cards()}
        {self.generate_charts_section()}
        {self.generate_repositories_section()}
        {self.generate_activity_section()}
        {self.generate_footer()}
    </div>
    
    <script>
        {self.generate_javascript()}
    </script>
</body>
</html>"""
        return html_content
    
    def generate_css(self) -> str:
        """Generate responsive CSS styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0D1117 0%, #161B22 100%);
            color: #C9D1D9;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header Styles */
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 0;
            background: rgba(22, 27, 34, 0.8);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(88, 166, 255, 0.2);
        }
        
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #58A6FF, #1F6FEB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            color: #8B949E;
            margin-bottom: 20px;
        }
        
        .last-updated {
            font-size: 0.9rem;
            color: #7C3AED;
            background: rgba(124, 58, 237, 0.1);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
        }
        
        /* Summary Cards */
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .summary-card {
            background: rgba(22, 27, 34, 0.9);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(88, 166, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .summary-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #58A6FF, #1F6FEB);
        }
        
        .summary-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(88, 166, 255, 0.2);
        }
        
        .card-icon {
            font-size: 2rem;
            margin-bottom: 15px;
            color: #58A6FF;
        }
        
        .card-title {
            font-size: 0.9rem;
            color: #8B949E;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        
        .card-value {
            font-size: 2.2rem;
            font-weight: bold;
            color: #C9D1D9;
            margin-bottom: 10px;
        }
        
        .card-change {
            font-size: 0.85rem;
            padding: 4px 8px;
            border-radius: 12px;
            display: inline-block;
        }
        
        .card-change.positive {
            background: rgba(46, 160, 67, 0.2);
            color: #2EA043;
        }
        
        .card-change.negative {
            background: rgba(248, 81, 73, 0.2);
            color: #F85149;
        }
        
        /* Charts Section */
        .charts-section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: #C9D1D9;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title i {
            color: #58A6FF;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .chart-container {
            background: rgba(22, 27, 34, 0.9);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(88, 166, 255, 0.2);
            height: 400px;
        }
        
        .chart-title {
            font-size: 1.2rem;
            margin-bottom: 20px;
            color: #C9D1D9;
            text-align: center;
        }
        
        /* Repositories Section */
        .repositories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .repo-card {
            background: rgba(22, 27, 34, 0.9);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(88, 166, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .repo-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(88, 166, 255, 0.15);
        }
        
        .repo-header {
            display: flex;
            justify-content: between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        
        .repo-name {
            font-size: 1.1rem;
            font-weight: bold;
            color: #58A6FF;
            text-decoration: none;
            flex: 1;
        }
        
        .repo-language {
            background: rgba(88, 166, 255, 0.2);
            color: #58A6FF;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        
        .repo-stats {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }
        
        .repo-stat {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9rem;
            color: #8B949E;
        }
        
        .health-score {
            margin-top: 15px;
        }
        
        .health-bar {
            width: 100%;
            height: 6px;
            background: rgba(139, 148, 158, 0.3);
            border-radius: 3px;
            overflow: hidden;
        }
        
        .health-fill {
            height: 100%;
            background: linear-gradient(90deg, #F85149, #FF8E53, #2EA043);
            border-radius: 3px;
            transition: width 0.5s ease;
        }
        
        /* Activity Section */
        .activity-timeline {
            background: rgba(22, 27, 34, 0.9);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(88, 166, 255, 0.2);
            margin-bottom: 40px;
        }
        
        .timeline-item {
            display: flex;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid rgba(139, 148, 158, 0.2);
        }
        
        .timeline-item:last-child {
            border-bottom: none;
        }
        
        .timeline-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(88, 166, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: #58A6FF;
        }
        
        .timeline-content {
            flex: 1;
        }
        
        .timeline-title {
            font-weight: bold;
            color: #C9D1D9;
            margin-bottom: 5px;
        }
        
        .timeline-description {
            color: #8B949E;
            font-size: 0.9rem;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 30px 0;
            color: #8B949E;
            border-top: 1px solid rgba(139, 148, 158, 0.2);
        }
        
        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .dashboard-container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .summary-cards {
                grid-template-columns: 1fr;
            }
            
            .charts-grid {
                grid-template-columns: 1fr;
            }
            
            .chart-container {
                height: 300px;
            }
            
            .repositories-grid {
                grid-template-columns: 1fr;
            }
            
            .repo-header {
                flex-direction: column;
                gap: 10px;
            }
            
            .repo-stats {
                flex-wrap: wrap;
            }
        }
        
        @media (max-width: 480px) {
            .header h1 {
                font-size: 1.5rem;
            }
            
            .card-value {
                font-size: 1.8rem;
            }
            
            .chart-container {
                height: 250px;
                padding: 15px;
            }
        }
        
        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(88, 166, 255, 0.3);
            border-radius: 50%;
            border-top-color: #58A6FF;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Animations */
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .slide-in {
            animation: slideIn 0.6s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateX(-30px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        """
    
    def generate_header(self) -> str:
        """Generate dashboard header"""
        user_data = self.data.get('user_data', {})
        username = user_data.get('login', 'GitHub User')
        
        return f"""
        <header class="header fade-in">
            <h1><i class="fab fa-github"></i> {username} Analytics Dashboard</h1>
            <p class="subtitle">Comprehensive GitHub Statistics & Insights</p>
            <div class="last-updated">
                <i class="fas fa-clock"></i> Last Updated: {datetime.fromisoformat(self.timestamp.replace('Z', '+00:00')).strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </header>
        """
    
    def generate_summary_cards(self) -> str:
        """Generate summary statistics cards"""
        summary = self.data.get('summary_metrics', {})
        activity = self.data.get('activity_metrics', {})
        
        cards_data = [
            {
                'icon': 'fas fa-code-branch',
                'title': 'Total Repositories',
                'value': summary.get('total_repositories', 0),
                'change': '+2 this month',
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-star',
                'title': 'Total Stars',
                'value': summary.get('total_stars', 0),
                'change': '+12 this week',
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-code-commit',
                'title': 'Commits This Month',
                'value': activity.get('commits_month', 0),
                'change': f"{activity.get('commits_week', 0)} this week",
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-fire',
                'title': 'Current Streak',
                'value': f"{activity.get('streak_days', 0)} days",
                'change': 'Keep it up!',
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-heart-pulse',
                'title': 'Health Score',
                'value': f"{summary.get('average_health_score', 0)}%",
                'change': 'Excellent',
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-users',
                'title': 'Community Engagement',
                'value': summary.get('community_engagement', 0),
                'change': 'Stars + Forks',
                'change_type': 'positive'
            }
        ]
        
        cards_html = '<div class="summary-cards">'
        for card in cards_data:
            cards_html += f"""
            <div class="summary-card slide-in">
                <div class="card-icon">
                    <i class="{card['icon']}"></i>
                </div>
                <div class="card-title">{card['title']}</div>
                <div class="card-value">{card['value']}</div>
                <div class="card-change {card['change_type']}">
                    {card['change']}
                </div>
            </div>
            """
        cards_html += '</div>'
        
        return cards_html
    
    def generate_charts_section(self) -> str:
        """Generate interactive charts section"""
        return f"""
        <section class="charts-section">
            <h2 class="section-title">
                <i class="fas fa-chart-line"></i>
                Analytics & Visualizations
            </h2>
            <div class="charts-grid">
                <div class="chart-container">
                    <h3 class="chart-title">Language Distribution</h3>
                    <canvas id="languageChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3 class="chart-title">Repository Health Scores</h3>
                    <canvas id="healthChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3 class="chart-title">Activity Timeline</h3>
                    <canvas id="activityChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3 class="chart-title">Stars vs Forks</h3>
                    <canvas id="starsForksChart"></canvas>
                </div>
            </div>
        </section>
        """
    
    def generate_repositories_section(self) -> str:
        """Generate repositories showcase section"""
        repositories = self.data.get('repositories', [])
        top_repos = sorted(repositories, key=lambda x: x.get('stars', 0), reverse=True)[:6]
        
        repos_html = f"""
        <section class="repositories-section">
            <h2 class="section-title">
                <i class="fas fa-folder-open"></i>
                Top Repositories
            </h2>
            <div class="repositories-grid">
        """
        
        for repo in top_repos:
            health_percentage = repo.get('health_score', 0)
            repos_html += f"""
            <div class="repo-card fade-in">
                <div class="repo-header">
                    <a href="https://github.com/{self.data.get('user_data', {}).get('login', '')}/{repo.get('name', '')}" 
                       class="repo-name" target="_blank">
                        {repo.get('name', 'Unknown')}
                    </a>
                    <span class="repo-language">{repo.get('language', 'Unknown')}</span>
                </div>
                <div class="repo-stats">
                    <div class="repo-stat">
                        <i class="fas fa-star"></i>
                        {repo.get('stars', 0)}
                    </div>
                    <div class="repo-stat">
                        <i class="fas fa-code-branch"></i>
                        {repo.get('forks', 0)}
                    </div>
                    <div class="repo-stat">
                        <i class="fas fa-exclamation-circle"></i>
                        {repo.get('issues', 0)}
                    </div>
                    <div class="repo-stat">
                        <i class="fas fa-users"></i>
                        {repo.get('contributors', 0)}
                    </div>
                </div>
                <div class="health-score">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-size: 0.9rem; color: #8B949E;">Health Score</span>
                        <span style="font-size: 0.9rem; color: #C9D1D9;">{health_percentage:.1f}%</span>
                    </div>
                    <div class="health-bar">
                        <div class="health-fill" style="width: {health_percentage}%"></div>
                    </div>
                </div>
            </div>
            """
        
        repos_html += """
            </div>
        </section>
        """
        
        return repos_html
    
    def generate_activity_section(self) -> str:
        """Generate activity timeline section"""
        activity = self.data.get('activity_metrics', {})
        
        timeline_items = [
            {
                'icon': 'fas fa-code-commit',
                'title': f"{activity.get('commits_today', 0)} commits today",
                'description': 'Keep up the great work!'
            },
            {
                'icon': 'fas fa-git-alt',
                'title': f"{activity.get('prs_opened', 0)} pull requests opened this month",
                'description': 'Contributing to the community'
            },
            {
                'icon': 'fas fa-check-circle',
                'title': f"{activity.get('prs_merged', 0)} pull requests merged",
                'description': 'Successful collaborations'
            },
            {
                'icon': 'fas fa-bug',
                'title': f"{activity.get('issues_closed', 0)} issues resolved",
                'description': 'Problem-solving in action'
            }
        ]
        
        timeline_html = f"""
        <section class="activity-section">
            <h2 class="section-title">
                <i class="fas fa-activity"></i>
                Recent Activity
            </h2>
            <div class="activity-timeline">
        """
        
        for item in timeline_items:
            timeline_html += f"""
            <div class="timeline-item">
                <div class="timeline-icon">
                    <i class="{item['icon']}"></i>
                </div>
                <div class="timeline-content">
                    <div class="timeline-title">{item['title']}</div>
                    <div class="timeline-description">{item['description']}</div>
                </div>
            </div>
            """
        
        timeline_html += """
            </div>
        </section>
        """
        
        return timeline_html
    
    def generate_footer(self) -> str:
        """Generate dashboard footer"""
        return f"""
        <footer class="footer">
            <p>
                <i class="fas fa-robot"></i>
                Generated automatically from GitHub API data
                <br>
                <small>Dashboard updates every 6 hours • Built with ❤️ for developers</small>
            </p>
        </footer>
        """
    
    def generate_javascript(self) -> str:
        """Generate JavaScript for interactive features"""
        languages_data = json.dumps(self.data.get('language_stats', []))
        repositories_data = json.dumps(self.data.get('repositories', []))
        activity_data = json.dumps(self.data.get('activity_metrics', {}))
        
        return f"""
        // Chart.js Configuration
        Chart.defaults.color = '#C9D1D9';
        Chart.defaults.borderColor = 'rgba(139, 148, 158, 0.2)';
        
        // Language Distribution Chart
        const languageData = {languages_data};
        const languageChart = new Chart(document.getElementById('languageChart'), {{
            type: 'doughnut',
            data: {{
                labels: languageData.map(lang => lang.name),
                datasets: [{{
                    data: languageData.map(lang => lang.percentage),
                    backgroundColor: [
                        '#58A6FF', '#1F6FEB', '#7C3AED', '#F85149',
                        '#2EA043', '#FF8E53', '#E3B341', '#8B949E'
                    ],
                    borderWidth: 2,
                    borderColor: '#0D1117'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true
                        }}
                    }}
                }}
            }}
        }});
        
        // Repository Health Chart
        const repoData = {repositories_data};
        const healthChart = new Chart(document.getElementById('healthChart'), {{
            type: 'bar',
            data: {{
                labels: repoData.slice(0, 8).map(repo => repo.name),
                datasets: [{{
                    label: 'Health Score',
                    data: repoData.slice(0, 8).map(repo => repo.health_score),
                    backgroundColor: 'rgba(88, 166, 255, 0.6)',
                    borderColor: '#58A6FF',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        grid: {{
                            color: 'rgba(139, 148, 158, 0.1)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            color: 'rgba(139, 148, 158, 0.1)'
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // Activity Timeline Chart
        const activityData = {activity_data};
        const activityChart = new Chart(document.getElementById('activityChart'), {{
            type: 'line',
            data: {{
                labels: ['Today', 'This Week', 'This Month'],
                datasets: [{{
                    label: 'Commits',
                    data: [
                        activityData.commits_today || 0,
                        activityData.commits_week || 0,
                        activityData.commits_month || 0
                    ],
                    borderColor: '#58A6FF',
                    backgroundColor: 'rgba(88, 166, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: 'rgba(139, 148, 158, 0.1)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            color: 'rgba(139, 148, 158, 0.1)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Stars vs Forks Scatter Chart
        const starsForksChart = new Chart(document.getElementById('starsForksChart'), {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: 'Repositories',
                    data: repoData.map(repo => ({{
                        x: repo.stars,
                        y: repo.forks
                    }})),
                    backgroundColor: 'rgba(88, 166, 255, 0.6)',
                    borderColor: '#58A6FF',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{
                        title: {{
                            display: true,
                            text: 'Stars'
                        }},
                        grid: {{
                            color: 'rgba(139, 148, 158, 0.1)'
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: 'Forks'
                        }},
                        grid: {{
                            color: 'rgba(139, 148, 158, 0.1)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
        
        // Add loading states
        function showLoading(elementId) {{
            const element = document.getElementById(elementId);
            element.innerHTML = '<div class="loading"></div>';
        }}
        
        // Animate cards on scroll
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        document.querySelectorAll('.summary-card, .repo-card').forEach(card => {{
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        }});
        
        // Auto-refresh functionality
        let refreshInterval;
        
        function startAutoRefresh() {{
            refreshInterval = setInterval(() => {{
                // In a real implementation, this would fetch new data
                console.log('Auto-refreshing dashboard data...');
            }}, 300000); // 5 minutes
        }}
        
        function stopAutoRefresh() {{
            if (refreshInterval) {{
                clearInterval(refreshInterval);
            }}
        }}
        
        // Start auto-refresh on load
        startAutoRefresh();
        
        // Stop auto-refresh when page is hidden
        document.addEventListener('visibilitychange', () => {{
            if (document.hidden) {{
                stopAutoRefresh();
            }} else {{
                startAutoRefresh();
            }}
        }});
        """

def generate_interactive_dashboard(analytics_data: Dict) -> str:
    """Main function to generate interactive dashboard"""
    generator = InteractiveDashboardGenerator(analytics_data)
    return generator.generate_dashboard()(analytics_data: Dict) -> str:
    """Generate interactive dashboard from analytics data"""
    generator = InteractiveDashboardGenerator(analytics_data)
    return generator.generate_dashboard()

def main():
    """Main function to generate dashboard from analytics data"""
    try:
        # Load analytics data
        with open('analytics-data.json', 'r') as f:
            analytics_data = json.load(f)
        
        # Generate dashboard
        dashboard_html = generate_interactive_dashboard(analytics_data)
        
        # Save dashboard
        with open('interactive-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        logger.info("Interactive dashboard generated successfully!")
        
    except FileNotFoundError:
        logger.error("Analytics data file not found. Run automated-analytics-updater.py first.")
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")

if __name__ == "__main__":
    main()