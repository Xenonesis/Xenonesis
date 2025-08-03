#!/usr/bin/env python3
"""
Working Dashboard Generator
Fixed version that generates HTML dashboards without import issues
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class WorkingDashboardGenerator:
    def __init__(self, analytics_data: Dict):
        self.data = analytics_data
        self.timestamp = analytics_data.get('timestamp', datetime.now().isoformat())
    
    def generate_complete_dashboard(self) -> str:
        """Generate complete interactive dashboard HTML"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Analytics Dashboard - {self.data.get('user_data', {}).get('login', 'User')}</title>
    
    <!-- External Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        {self.generate_footer()}
    </div>
    
    <script>
        {self.generate_javascript()}
    </script>
</body>
</html>"""
    
    def generate_css(self) -> str:
        """Generate CSS styles"""
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
            text-align: center;
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
            background: rgba(46, 160, 67, 0.2);
            color: #2EA043;
        }
        
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
            justify-content: center;
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
            justify-content: space-between;
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
        
        .footer {
            text-align: center;
            padding: 30px 0;
            color: #8B949E;
            border-top: 1px solid rgba(139, 148, 158, 0.2);
        }
        
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
        }
        """
    
    def generate_header(self) -> str:
        """Generate dashboard header"""
        user_data = self.data.get('user_data', {})
        username = user_data.get('login', 'GitHub User')
        
        return f"""
        <header class="header">
            <h1><i class="fab fa-github"></i> {username} Analytics Dashboard</h1>
            <p class="subtitle">Comprehensive GitHub Statistics & Insights</p>
            <div class="last-updated">
                <i class="fas fa-clock"></i> Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
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
                'change': '+2 this month'
            },
            {
                'icon': 'fas fa-star',
                'title': 'Total Stars',
                'value': summary.get('total_stars', 0),
                'change': '+12 this week'
            },
            {
                'icon': 'fas fa-code-commit',
                'title': 'Commits This Month',
                'value': activity.get('commits_month', 0),
                'change': f"{activity.get('commits_week', 0)} this week"
            },
            {
                'icon': 'fas fa-fire',
                'title': 'Current Streak',
                'value': f"{activity.get('streak_days', 0)} days",
                'change': 'Keep it up!'
            },
            {
                'icon': 'fas fa-heart-pulse',
                'title': 'Health Score',
                'value': f"{summary.get('average_health_score', 0):.0f}%",
                'change': 'Excellent'
            },
            {
                'icon': 'fas fa-users',
                'title': 'Community Engagement',
                'value': summary.get('community_engagement', 0),
                'change': 'Stars + Forks'
            }
        ]
        
        cards_html = '<div class="summary-cards">'
        for card in cards_data:
            cards_html += f"""
            <div class="summary-card">
                <div class="card-icon">
                    <i class="{card['icon']}"></i>
                </div>
                <div class="card-title">{card['title']}</div>
                <div class="card-value">{card['value']}</div>
                <div class="card-change">
                    {card['change']}
                </div>
            </div>
            """
        cards_html += '</div>'
        
        return cards_html
    
    def generate_charts_section(self) -> str:
        """Generate charts section"""
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
            </div>
        </section>
        """
    
    def generate_repositories_section(self) -> str:
        """Generate repositories section"""
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
            <div class="repo-card">
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
    
    def generate_footer(self) -> str:
        """Generate footer"""
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
        """Generate JavaScript for charts"""
        languages_data = json.dumps(self.data.get('language_stats', []))
        repositories_data = json.dumps(self.data.get('repositories', []))
        
        return f"""
        // Chart.js Configuration
        Chart.defaults.color = '#C9D1D9';
        Chart.defaults.borderColor = 'rgba(139, 148, 158, 0.2)';
        
        // Language Distribution Chart
        const languageData = {languages_data};
        if (languageData.length > 0) {{
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
        }}
        
        // Repository Health Chart
        const repoData = {repositories_data};
        if (repoData.length > 0) {{
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
        }}
        """

def create_sample_data():
    """Create sample analytics data"""
    return {
        'timestamp': datetime.now().isoformat(),
        'user_data': {
            'login': 'Xenonesis',
            'name': 'GitHub User',
            'public_repos': 25,
            'followers': 50
        },
        'summary_metrics': {
            'total_repositories': 25,
            'total_stars': 150,
            'total_forks': 45,
            'average_health_score': 85.5,
            'active_repositories': 20,
            'community_engagement': 195,
            'productivity_score': 92.3
        },
        'activity_metrics': {
            'commits_today': 3,
            'commits_week': 15,
            'commits_month': 67,
            'prs_opened': 8,
            'prs_merged': 6,
            'issues_opened': 4,
            'issues_closed': 7,
            'streak_days': 23
        },
        'language_stats': [
            {'name': 'Python', 'percentage': 45.2, 'repos': 12},
            {'name': 'JavaScript', 'percentage': 28.7, 'repos': 8},
            {'name': 'TypeScript', 'percentage': 15.1, 'repos': 4},
            {'name': 'Go', 'percentage': 8.3, 'repos': 2},
            {'name': 'Rust', 'percentage': 2.7, 'repos': 1}
        ],
        'repositories': [
            {
                'name': 'cybersecurity-toolkit',
                'stars': 45,
                'forks': 12,
                'issues': 3,
                'language': 'Python',
                'health_score': 92.5,
                'contributors': 8,
                'last_updated': '2025-01-30T10:30:00Z'
            },
            {
                'name': 'ai-ml-projects',
                'stars': 38,
                'forks': 9,
                'issues': 1,
                'language': 'Python',
                'health_score': 88.2,
                'contributors': 5,
                'last_updated': '2025-01-29T15:45:00Z'
            },
            {
                'name': 'network-security-scanner',
                'stars': 32,
                'forks': 7,
                'issues': 2,
                'language': 'Go',
                'health_score': 95.1,
                'contributors': 3,
                'last_updated': '2025-01-28T09:20:00Z'
            },
            {
                'name': 'blockchain-analyzer',
                'stars': 28,
                'forks': 6,
                'issues': 0,
                'language': 'Rust',
                'health_score': 89.7,
                'contributors': 4,
                'last_updated': '2025-01-27T14:15:00Z'
            },
            {
                'name': 'web-vulnerability-scanner',
                'stars': 24,
                'forks': 5,
                'issues': 1,
                'language': 'JavaScript',
                'health_score': 86.3,
                'contributors': 6,
                'last_updated': '2025-01-26T11:30:00Z'
            }
        ],
        'collection_info': {
            'total_repos': 25,
            'rate_limit_remaining': 4500
        }
    }

def main():
    print("🚀 Working Dashboard Generator")
    print("=" * 50)
    
    try:
        # Create sample data
        sample_data = create_sample_data()
        print("✅ Sample data created")
        
        # Generate dashboard
        generator = WorkingDashboardGenerator(sample_data)
        html_content = generator.generate_complete_dashboard()
        
        # Save to file
        filename = 'working-dashboard.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        file_size = os.path.getsize(filename)
        
        print(f"✅ Dashboard generated successfully!")
        print(f"   File: {filename}")
        print(f"   Size: {file_size} bytes")
        print(f"   Characters: {len(html_content)}")
        
        print("\n🌐 How to view:")
        print("1. Double-click the HTML file")
        print("2. Or drag it into your browser")
        print("3. Or use: start working-dashboard.html")
        
        # Try to open automatically
        try:
            import webbrowser
            webbrowser.open(filename)
            print(f"\n🚀 Opening {filename} in your browser...")
        except:
            print("\n⚠️ Please open the file manually in your browser")
        
        print("\n✨ This dashboard includes:")
        print("• Interactive charts with Chart.js")
        print("• Responsive design for mobile/desktop")
        print("• Real GitHub-style dark theme")
        print("• Repository cards with health scores")
        print("• Summary statistics cards")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Details: {traceback.format_exc()}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()