#!/usr/bin/env python3
"""
Mobile-Responsive Analytics Updater
Generates mobile-optimized HTML components and responsive layouts
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class MobileResponsiveUpdater:
    def __init__(self, analytics_data: Dict):
        self.data = analytics_data
        self.breakpoints = {
            'mobile': '480px',
            'tablet': '768px',
            'desktop': '1024px',
            'large': '1200px'
        }
    
    def generate_responsive_css(self) -> str:
        """Generate comprehensive responsive CSS"""
        return f"""
        /* Mobile-First Responsive Design */
        :root {{
            --primary-color: #58A6FF;
            --secondary-color: #1F6FEB;
            --accent-color: #7C3AED;
            --success-color: #2EA043;
            --warning-color: #FF8E53;
            --error-color: #F85149;
            --bg-primary: #0D1117;
            --bg-secondary: #161B22;
            --bg-tertiary: #21262D;
            --text-primary: #C9D1D9;
            --text-secondary: #8B949E;
            --border-color: rgba(88, 166, 255, 0.2);
            --shadow-light: 0 2px 8px rgba(0, 0, 0, 0.1);
            --shadow-medium: 0 4px 16px rgba(0, 0, 0, 0.2);
            --shadow-heavy: 0 8px 32px rgba(0, 0, 0, 0.3);
            --border-radius: 12px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            font-size: 14px; /* Base font size for mobile */
            scroll-behavior: smooth;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        /* Container System */
        .container {{
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 16px;
        }}
        
        .container-fluid {{
            width: 100%;
            padding: 0 16px;
        }}
        
        /* Grid System */
        .row {{
            display: flex;
            flex-wrap: wrap;
            margin: 0 -8px;
        }}
        
        .col {{
            flex: 1;
            padding: 0 8px;
            min-width: 0;
        }}
        
        .col-12 {{ width: 100%; }}
        .col-6 {{ width: 50%; }}
        .col-4 {{ width: 33.333%; }}
        .col-3 {{ width: 25%; }}
        
        /* Mobile Grid (default) */
        .col-sm-12 {{ width: 100%; }}
        .col-sm-6 {{ width: 50%; }}
        .col-sm-4 {{ width: 33.333%; }}
        .col-sm-3 {{ width: 25%; }}
        
        /* Header Styles */
        .mobile-header {{
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(13, 17, 23, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            padding: 12px 0;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .logo {{
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        .mobile-menu-toggle {{
            display: none;
            background: none;
            border: none;
            color: var(--text-primary);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 8px;
        }}
        
        .nav-menu {{
            display: flex;
            list-style: none;
            gap: 20px;
        }}
        
        .nav-menu a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            transition: var(--transition);
            padding: 8px 12px;
            border-radius: 6px;
        }}
        
        .nav-menu a:hover {{
            color: var(--primary-color);
            background: rgba(88, 166, 255, 0.1);
        }}
        
        /* Card Components */
        .card {{
            background: var(--bg-secondary);
            border-radius: var(--border-radius);
            border: 1px solid var(--border-color);
            overflow: hidden;
            transition: var(--transition);
            margin-bottom: 20px;
        }}
        
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-medium);
        }}
        
        .card-header {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
            background: rgba(88, 166, 255, 0.05);
        }}
        
        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }}
        
        .card-body {{
            padding: 20px;
        }}
        
        .card-footer {{
            padding: 12px 20px;
            background: rgba(139, 148, 158, 0.05);
            border-top: 1px solid var(--border-color);
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        /* Metric Cards */
        .metric-card {{
            background: var(--bg-secondary);
            border-radius: var(--border-radius);
            padding: 20px;
            border: 1px solid var(--border-color);
            text-align: center;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-medium);
        }}
        
        .metric-icon {{
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 12px;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--text-primary);
            margin-bottom: 8px;
            line-height: 1;
        }}
        
        .metric-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .metric-change {{
            font-size: 0.8rem;
            padding: 4px 8px;
            border-radius: 12px;
            display: inline-block;
        }}
        
        .metric-change.positive {{
            background: rgba(46, 160, 67, 0.2);
            color: var(--success-color);
        }}
        
        .metric-change.negative {{
            background: rgba(248, 81, 73, 0.2);
            color: var(--error-color);
        }}
        
        /* Chart Containers */
        .chart-wrapper {{
            background: var(--bg-secondary);
            border-radius: var(--border-radius);
            padding: 20px;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
        }}
        
        .chart-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 16px;
            text-align: center;
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
            width: 100%;
        }}
        
        /* Repository Cards */
        .repo-card {{
            background: var(--bg-secondary);
            border-radius: var(--border-radius);
            padding: 20px;
            border: 1px solid var(--border-color);
            transition: var(--transition);
            margin-bottom: 16px;
        }}
        
        .repo-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-light);
        }}
        
        .repo-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .repo-name {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary-color);
            text-decoration: none;
            flex: 1;
            min-width: 0;
        }}
        
        .repo-language {{
            background: rgba(88, 166, 255, 0.2);
            color: var(--primary-color);
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            white-space: nowrap;
        }}
        
        .repo-description {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 12px;
            line-height: 1.4;
        }}
        
        .repo-stats {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}
        
        .repo-stat {{
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        .repo-stat i {{
            font-size: 0.8rem;
        }}
        
        /* Progress Bars */
        .progress {{
            width: 100%;
            height: 8px;
            background: rgba(139, 148, 158, 0.2);
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0;
        }}
        
        .progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        
        /* Buttons */
        .btn {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            text-align: center;
            transition: var(--transition);
            border: none;
            cursor: pointer;
            line-height: 1;
        }}
        
        .btn-primary {{
            background: var(--primary-color);
            color: white;
        }}
        
        .btn-primary:hover {{
            background: var(--secondary-color);
            transform: translateY(-1px);
        }}
        
        .btn-secondary {{
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }}
        
        .btn-secondary:hover {{
            background: var(--bg-secondary);
        }}
        
        .btn-sm {{
            padding: 6px 12px;
            font-size: 0.8rem;
        }}
        
        /* Utilities */
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        
        .mb-0 {{ margin-bottom: 0; }}
        .mb-1 {{ margin-bottom: 8px; }}
        .mb-2 {{ margin-bottom: 16px; }}
        .mb-3 {{ margin-bottom: 24px; }}
        .mb-4 {{ margin-bottom: 32px; }}
        
        .mt-0 {{ margin-top: 0; }}
        .mt-1 {{ margin-top: 8px; }}
        .mt-2 {{ margin-top: 16px; }}
        .mt-3 {{ margin-top: 24px; }}
        .mt-4 {{ margin-top: 32px; }}
        
        .p-0 {{ padding: 0; }}
        .p-1 {{ padding: 8px; }}
        .p-2 {{ padding: 16px; }}
        .p-3 {{ padding: 24px; }}
        .p-4 {{ padding: 32px; }}
        
        .d-none {{ display: none; }}
        .d-block {{ display: block; }}
        .d-flex {{ display: flex; }}
        .d-grid {{ display: grid; }}
        
        .flex-wrap {{ flex-wrap: wrap; }}
        .flex-nowrap {{ flex-wrap: nowrap; }}
        .justify-center {{ justify-content: center; }}
        .justify-between {{ justify-content: space-between; }}
        .align-center {{ align-items: center; }}
        
        /* Loading States */
        .loading {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(88, 166, 255, 0.3);
            border-radius: 50%;
            border-top-color: var(--primary-color);
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        .skeleton {{
            background: linear-gradient(90deg, 
                rgba(139, 148, 158, 0.1) 25%, 
                rgba(139, 148, 158, 0.2) 50%, 
                rgba(139, 148, 158, 0.1) 75%
            );
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }}
        
        @keyframes loading {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}
        
        /* Tablet Styles */
        @media (min-width: {self.breakpoints['tablet']}) {{
            html {{ font-size: 15px; }}
            
            .container {{ padding: 0 24px; }}
            .container-fluid {{ padding: 0 24px; }}
            
            .row {{ margin: 0 -12px; }}
            .col {{ padding: 0 12px; }}
            
            .col-md-12 {{ width: 100%; }}
            .col-md-6 {{ width: 50%; }}
            .col-md-4 {{ width: 33.333%; }}
            .col-md-3 {{ width: 25%; }}
            .col-md-2 {{ width: 16.666%; }}
            
            .mobile-menu-toggle {{ display: none; }}
            
            .metric-card {{
                padding: 24px;
            }}
            
            .metric-value {{
                font-size: 2.2rem;
            }}
            
            .chart-container {{
                height: 350px;
            }}
            
            .repo-header {{
                flex-wrap: nowrap;
            }}
        }}
        
        /* Desktop Styles */
        @media (min-width: {self.breakpoints['desktop']}) {{
            html {{ font-size: 16px; }}
            
            .container {{ padding: 0 32px; }}
            .container-fluid {{ padding: 0 32px; }}
            
            .row {{ margin: 0 -16px; }}
            .col {{ padding: 0 16px; }}
            
            .col-lg-12 {{ width: 100%; }}
            .col-lg-6 {{ width: 50%; }}
            .col-lg-4 {{ width: 33.333%; }}
            .col-lg-3 {{ width: 25%; }}
            .col-lg-2 {{ width: 16.666%; }}
            
            .metric-card {{
                padding: 28px;
            }}
            
            .metric-value {{
                font-size: 2.5rem;
            }}
            
            .chart-container {{
                height: 400px;
            }}
        }}
        
        /* Large Desktop Styles */
        @media (min-width: {self.breakpoints['large']}) {{
            .col-xl-12 {{ width: 100%; }}
            .col-xl-6 {{ width: 50%; }}
            .col-xl-4 {{ width: 33.333%; }}
            .col-xl-3 {{ width: 25%; }}
            .col-xl-2 {{ width: 16.666%; }}
        }}
        
        /* Mobile-specific styles */
        @media (max-width: {self.breakpoints['mobile']}) {{
            html {{ font-size: 13px; }}
            
            .container {{ padding: 0 12px; }}
            .container-fluid {{ padding: 0 12px; }}
            
            .mobile-menu-toggle {{ display: block; }}
            
            .nav-menu {{
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--bg-primary);
                border-top: 1px solid var(--border-color);
                flex-direction: column;
                padding: 16px;
                gap: 8px;
            }}
            
            .nav-menu.active {{
                display: flex;
            }}
            
            .metric-card {{
                padding: 16px;
            }}
            
            .metric-value {{
                font-size: 1.8rem;
            }}
            
            .chart-container {{
                height: 250px;
            }}
            
            .repo-stats {{
                gap: 12px;
            }}
            
            .repo-stat {{
                font-size: 0.8rem;
            }}
            
            .btn {{
                padding: 8px 16px;
                font-size: 0.85rem;
            }}
            
            .card-body {{
                padding: 16px;
            }}
            
            .card-header {{
                padding: 12px 16px;
            }}
        }}
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-primary: #0D1117;
                --bg-secondary: #161B22;
                --bg-tertiary: #21262D;
                --text-primary: #C9D1D9;
                --text-secondary: #8B949E;
            }}
        }}
        
        /* High contrast mode */
        @media (prefers-contrast: high) {{
            :root {{
                --border-color: rgba(255, 255, 255, 0.3);
                --text-secondary: #A5A5A5;
            }}
        }}
        
        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        /* Print styles */
        @media print {{
            .mobile-header,
            .nav-menu,
            .btn {{
                display: none;
            }}
            
            .card {{
                break-inside: avoid;
                border: 1px solid #000;
            }}
            
            body {{
                background: white;
                color: black;
            }}
        }}
        """
    
    def generate_mobile_optimized_html(self) -> str:
        """Generate mobile-optimized HTML structure"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <meta name="theme-color" content="#58A6FF">
    <meta name="description" content="GitHub Analytics Dashboard - Mobile Optimized">
    <title>GitHub Analytics - Mobile Dashboard</title>
    
    <!-- Preload critical resources -->
    <link rel="preload" href="https://cdn.jsdelivr.net/npm/chart.js" as="script">
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" as="style">
    
    <!-- External Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    
    <style>
        {self.generate_responsive_css()}
    </style>
</head>
<body>
    <!-- Mobile Header -->
    <header class="mobile-header">
        <div class="container">
            <div class="header-content">
                <a href="#" class="logo">
                    <i class="fab fa-github"></i> Analytics
                </a>
                <button class="mobile-menu-toggle" onclick="toggleMobileMenu()">
                    <i class="fas fa-bars"></i>
                </button>
                <nav class="nav-menu" id="mobileMenu">
                    <a href="#overview">Overview</a>
                    <a href="#repositories">Repositories</a>
                    <a href="#languages">Languages</a>
                    <a href="#activity">Activity</a>
                </nav>
            </div>
        </div>
    </header>
    
    <!-- Main Content -->
    <main class="container">
        {self.generate_overview_section()}
        {self.generate_metrics_grid()}
        {self.generate_charts_section()}
        {self.generate_repositories_section()}
        {self.generate_activity_section()}
    </main>
    
    <!-- Footer -->
    <footer class="text-center p-4 mt-4">
        <p style="color: var(--text-secondary); font-size: 0.85rem;">
            <i class="fas fa-mobile-alt"></i> Mobile-optimized dashboard
            <br>
            <small>Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</small>
        </p>
    </footer>
    
    <script>
        {self.generate_mobile_javascript()}
    </script>
</body>
</html>"""
    
    def generate_overview_section(self) -> str:
        """Generate mobile-optimized overview section"""
        user_data = self.data.get('user_data', {})
        summary = self.data.get('summary_metrics', {})
        
        return f"""
        <section id="overview" class="mt-3 mb-4">
            <div class="card">
                <div class="card-header text-center">
                    <h1 class="card-title">
                        <i class="fab fa-github"></i> 
                        {user_data.get('login', 'GitHub User')}
                    </h1>
                    <p style="color: var(--text-secondary); margin: 8px 0 0 0;">
                        GitHub Analytics Dashboard
                    </p>
                </div>
                <div class="card-body text-center">
                    <div class="row">
                        <div class="col-6 col-md-3">
                            <div class="metric-value">{summary.get('total_repositories', 0)}</div>
                            <div class="metric-label">Repositories</div>
                        </div>
                        <div class="col-6 col-md-3">
                            <div class="metric-value">{summary.get('total_stars', 0)}</div>
                            <div class="metric-label">Stars</div>
                        </div>
                        <div class="col-6 col-md-3">
                            <div class="metric-value">{summary.get('total_forks', 0)}</div>
                            <div class="metric-label">Forks</div>
                        </div>
                        <div class="col-6 col-md-3">
                            <div class="metric-value">{summary.get('average_health_score', 0):.0f}%</div>
                            <div class="metric-label">Health Score</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def generate_metrics_grid(self) -> str:
        """Generate responsive metrics grid"""
        activity = self.data.get('activity_metrics', {})
        summary = self.data.get('summary_metrics', {})
        
        metrics = [
            {
                'icon': 'fas fa-code-commit',
                'value': activity.get('commits_month', 0),
                'label': 'Commits This Month',
                'change': f"+{activity.get('commits_week', 0)} this week",
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-fire',
                'value': f"{activity.get('streak_days', 0)} days",
                'label': 'Current Streak',
                'change': 'Keep going!',
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-users',
                'value': summary.get('community_engagement', 0),
                'label': 'Community Engagement',
                'change': 'Stars + Forks',
                'change_type': 'positive'
            },
            {
                'icon': 'fas fa-chart-line',
                'value': f"{summary.get('productivity_score', 0):.0f}%",
                'label': 'Productivity Score',
                'change': 'Excellent',
                'change_type': 'positive'
            }
        ]
        
        metrics_html = '<section id="metrics" class="mb-4"><div class="row">'
        
        for metric in metrics:
            metrics_html += f"""
            <div class="col-6 col-md-3 mb-3">
                <div class="metric-card">
                    <div class="metric-icon">
                        <i class="{metric['icon']}"></i>
                    </div>
                    <div class="metric-value">{metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                    <div class="metric-change {metric['change_type']}">
                        {metric['change']}
                    </div>
                </div>
            </div>
            """
        
        metrics_html += '</div></section>'
        return metrics_html
    
    def generate_charts_section(self) -> str:
        """Generate mobile-optimized charts section"""
        return f"""
        <section id="charts" class="mb-4">
            <h2 class="text-center mb-3">
                <i class="fas fa-chart-pie"></i> Analytics
            </h2>
            <div class="row">
                <div class="col-12 col-lg-6 mb-3">
                    <div class="chart-wrapper">
                        <h3 class="chart-title">Language Distribution</h3>
                        <div class="chart-container">
                            <canvas id="mobileLanguageChart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-lg-6 mb-3">
                    <div class="chart-wrapper">
                        <h3 class="chart-title">Repository Health</h3>
                        <div class="chart-container">
                            <canvas id="mobileHealthChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def generate_repositories_section(self) -> str:
        """Generate mobile-optimized repositories section"""
        repositories = self.data.get('repositories', [])
        top_repos = sorted(repositories, key=lambda x: x.get('stars', 0), reverse=True)[:6]
        
        repos_html = f"""
        <section id="repositories" class="mb-4">
            <h2 class="text-center mb-3">
                <i class="fas fa-folder-open"></i> Top Repositories
            </h2>
            <div class="row">
        """
        
        for repo in top_repos:
            health_score = repo.get('health_score', 0)
            repos_html += f"""
            <div class="col-12 col-md-6 col-lg-4 mb-3">
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
                    <div class="mt-2">
                        <div class="d-flex justify-between align-center mb-1">
                            <span style="font-size: 0.8rem; color: var(--text-secondary);">Health</span>
                            <span style="font-size: 0.8rem; color: var(--text-primary);">{health_score:.0f}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" style="width: {health_score}%"></div>
                        </div>
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
        """Generate mobile-optimized activity section"""
        activity = self.data.get('activity_metrics', {})
        
        return f"""
        <section id="activity" class="mb-4">
            <h2 class="text-center mb-3">
                <i class="fas fa-activity"></i> Recent Activity
            </h2>
            <div class="card">
                <div class="card-body">
                    <div class="row text-center">
                        <div class="col-6 col-md-3 mb-3">
                            <div class="metric-value" style="font-size: 1.5rem;">{activity.get('commits_today', 0)}</div>
                            <div class="metric-label">Today</div>
                        </div>
                        <div class="col-6 col-md-3 mb-3">
                            <div class="metric-value" style="font-size: 1.5rem;">{activity.get('commits_week', 0)}</div>
                            <div class="metric-label">This Week</div>
                        </div>
                        <div class="col-6 col-md-3 mb-3">
                            <div class="metric-value" style="font-size: 1.5rem;">{activity.get('prs_opened', 0)}</div>
                            <div class="metric-label">PRs Opened</div>
                        </div>
                        <div class="col-6 col-md-3 mb-3">
                            <div class="metric-value" style="font-size: 1.5rem;">{activity.get('issues_closed', 0)}</div>
                            <div class="metric-label">Issues Closed</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def generate_mobile_javascript(self) -> str:
        """Generate mobile-optimized JavaScript"""
        languages_data = json.dumps(self.data.get('language_stats', []))
        repositories_data = json.dumps(self.data.get('repositories', []))
        
        return f"""
        // Mobile menu toggle
        function toggleMobileMenu() {{
            const menu = document.getElementById('mobileMenu');
            menu.classList.toggle('active');
        }}
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {{
            const menu = document.getElementById('mobileMenu');
            const toggle = document.querySelector('.mobile-menu-toggle');
            
            if (!menu.contains(event.target) && !toggle.contains(event.target)) {{
                menu.classList.remove('active');
            }}
        }});
        
        // Chart.js mobile configuration
        Chart.defaults.responsive = true;
        Chart.defaults.maintainAspectRatio = false;
        Chart.defaults.color = '#C9D1D9';
        Chart.defaults.borderColor = 'rgba(139, 148, 158, 0.2)';
        
        // Language chart
        const languageData = {languages_data};
        if (languageData.length > 0) {{
            new Chart(document.getElementById('mobileLanguageChart'), {{
                type: 'doughnut',
                data: {{
                    labels: languageData.slice(0, 6).map(lang => lang.name),
                    datasets: [{{
                        data: languageData.slice(0, 6).map(lang => lang.percentage),
                        backgroundColor: [
                            '#58A6FF', '#1F6FEB', '#7C3AED', '#F85149',
                            '#2EA043', '#FF8E53'
                        ],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{
                                padding: 15,
                                usePointStyle: true,
                                font: {{
                                    size: 11
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Health chart
        const repoData = {repositories_data};
        if (repoData.length > 0) {{
            new Chart(document.getElementById('mobileHealthChart'), {{
                type: 'bar',
                data: {{
                    labels: repoData.slice(0, 6).map(repo => repo.name.length > 10 ? repo.name.substring(0, 10) + '...' : repo.name),
                    datasets: [{{
                        label: 'Health Score',
                        data: repoData.slice(0, 6).map(repo => repo.health_score),
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
                            }},
                            ticks: {{
                                font: {{
                                    size: 10
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{
                                color: 'rgba(139, 148, 158, 0.1)'
                            }},
                            ticks: {{
                                font: {{
                                    size: 10
                                }}
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
        
        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                    // Close mobile menu
                    document.getElementById('mobileMenu').classList.remove('active');
                }}
            }});
        }});
        
        // Intersection Observer for animations
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
        
        // Observe elements for animation
        document.querySelectorAll('.metric-card, .repo-card, .chart-wrapper').forEach(el => {{
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        }});
        
        // Touch gestures for mobile
        let touchStartX = 0;
        let touchEndX = 0;
        
        document.addEventListener('touchstart', e => {{
            touchStartX = e.changedTouches[0].screenX;
        }});
        
        document.addEventListener('touchend', e => {{
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }});
        
        function handleSwipe() {{
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > swipeThreshold) {{
                if (diff > 0) {{
                    // Swipe left - could implement navigation
                    console.log('Swiped left');
                }} else {{
                    // Swipe right - could implement navigation
                    console.log('Swiped right');
                }}
            }}
        }}
        
        // Performance monitoring
        if ('performance' in window) {{
            window.addEventListener('load', () => {{
                const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
                console.log('Page load time:', loadTime + 'ms');
            }});
        }}
        
        // Service Worker registration for PWA
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => {{
                        console.log('SW registered: ', registration);
                    }})
                    .catch(registrationError => {{
                        console.log('SW registration failed: ', registrationError);
                    }});
            }});
        }}
        """

def generate_mobile_dashboard(analytics_data: Dict) -> str:
    """Generate mobile-optimized dashboard"""
    updater = MobileResponsiveUpdater(analytics_data)
    return updater.generate_mobile_optimized_html()

def main():
    """Main function to generate mobile dashboard"""
    try:
        # Load analytics data
        with open('analytics-data.json', 'r') as f:
            analytics_data = json.load(f)
        
        # Generate mobile dashboard
        mobile_html = generate_mobile_dashboard(analytics_data)
        
        # Save mobile dashboard
        with open('mobile-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(mobile_html)
        
        logger.info("Mobile-responsive dashboard generated successfully!")
        
    except FileNotFoundError:
        logger.error("Analytics data file not found. Run automated-analytics-updater.py first.")
    except Exception as e:
        logger.error(f"Error generating mobile dashboard: {e}")

if __name__ == "__main__":
    main()  
  def generate_mobile_javascript(self) -> str:
        """Generate mobile-optimized JavaScript"""
        languages_data = json.dumps(self.data.get('language_stats', []))
        repositories_data = json.dumps(self.data.get('repositories', []))
        
        return f"""
        // Mobile Menu Toggle
        function toggleMobileMenu() {{
            const menu = document.getElementById('mobileMenu');
            menu.classList.toggle('active');
        }}
        
        // Chart.js Mobile Configuration
        Chart.defaults.color = '#C9D1D9';
        Chart.defaults.borderColor = 'rgba(139, 148, 158, 0.2)';
        
        // Mobile Language Chart
        const languageData = {languages_data};
        if (languageData.length > 0) {{
            const mobileLanguageChart = new Chart(document.getElementById('mobileLanguageChart'), {{
                type: 'doughnut',
                data: {{
                    labels: languageData.slice(0, 6).map(lang => lang.name),
                    datasets: [{{
                        data: languageData.slice(0, 6).map(lang => lang.percentage),
                        backgroundColor: [
                            '#58A6FF', '#1F6FEB', '#7C3AED', '#F85149',
                            '#2EA043', '#FF8E53'
                        ],
                        borderWidth: 1,
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
                                padding: 15,
                                usePointStyle: true,
                                font: {{
                                    size: 11
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Mobile Health Chart
        const repoData = {repositories_data};
        if (repoData.length > 0) {{
            const mobileHealthChart = new Chart(document.getElementById('mobileHealthChart'), {{
                type: 'bar',
                data: {{
                    labels: repoData.slice(0, 5).map(repo => repo.name.length > 10 ? repo.name.substring(0, 10) + '...' : repo.name),
                    datasets: [{{
                        label: 'Health',
                        data: repoData.slice(0, 5).map(repo => repo.health_score),
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
                            }},
                            ticks: {{
                                font: {{
                                    size: 10
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{
                                color: 'rgba(139, 148, 158, 0.1)'
                            }},
                            ticks: {{
                                font: {{
                                    size: 10
                                }}
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
        
        // Touch gestures for mobile
        let touchStartX = 0;
        let touchEndX = 0;
        
        document.addEventListener('touchstart', function(event) {{
            touchStartX = event.changedTouches[0].screenX;
        }});
        
        document.addEventListener('touchend', function(event) {{
            touchEndX = event.changedTouches[0].screenX;
            handleSwipe();
        }});
        
        function handleSwipe() {{
            if (touchEndX < touchStartX - 50) {{
                // Swipe left - could implement navigation
                console.log('Swiped left');
            }}
            if (touchEndX > touchStartX + 50) {{
                // Swipe right - could implement navigation
                console.log('Swiped right');
            }}
        }}
        
        // Intersection Observer for animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -30px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);
        
        // Observe elements for animation
        document.querySelectorAll('.metric-card, .repo-card, .chart-wrapper').forEach(element => {{
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(element);
        }});
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {{
            const menu = document.getElementById('mobileMenu');
            const toggle = document.querySelector('.mobile-menu-toggle');
            
            if (!menu.contains(event.target) && !toggle.contains(event.target)) {{
                menu.classList.remove('active');
            }}
        }});
        
        // Prevent zoom on double tap for iOS
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {{
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {{
                event.preventDefault();
            }}
            lastTouchEnd = now;
        }}, false);
        """

def generate_mobile_dashboard(analytics_data: Dict) -> str:
    """Main function to generate mobile dashboard"""
    generator = MobileResponsiveUpdater(analytics_data)
    return generator.generate_mobile_optimized_html()