#!/usr/bin/env python3
"""
Test Dashboard Generation
Simple script to test HTML dashboard generation without full analytics pipeline
"""

import json
import os
from datetime import datetime

def create_sample_data():
    """Create sample analytics data for testing"""
    return {
        'timestamp': datetime.now().isoformat(),
        'user_data': {
            'login': 'TestUser',
            'name': 'Test User',
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
                'name': 'awesome-project',
                'stars': 45,
                'forks': 12,
                'issues': 3,
                'language': 'Python',
                'health_score': 92.5,
                'contributors': 8,
                'last_updated': '2025-01-30T10:30:00Z'
            },
            {
                'name': 'web-app',
                'stars': 32,
                'forks': 8,
                'issues': 1,
                'language': 'JavaScript',
                'health_score': 88.2,
                'contributors': 5,
                'last_updated': '2025-01-29T15:45:00Z'
            },
            {
                'name': 'api-service',
                'stars': 28,
                'forks': 6,
                'issues': 2,
                'language': 'Go',
                'health_score': 95.1,
                'contributors': 3,
                'last_updated': '2025-01-28T09:20:00Z'
            }
        ],
        'collection_info': {
            'total_repos': 25,
            'rate_limit_remaining': 4500
        }
    }

def test_dashboard_generation():
    """Test dashboard generation with sample data"""
    print("🧪 Testing Dashboard Generation")
    print("=" * 50)
    
    # Create sample data
    sample_data = create_sample_data()
    print("✅ Sample data created")
    
    try:
        # Test interactive dashboard
        print("\n📱 Testing Interactive Dashboard...")
        import sys
        sys.path.append('scripts')
        
        from scripts.interactive_dashboard_generator import InteractiveDashboardGenerator
        
        interactive_generator = InteractiveDashboardGenerator(sample_data)
        interactive_html = interactive_generator.generate_dashboard()
        
        # Save to file
        with open('test-interactive-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(interactive_html)
        
        print(f"✅ Interactive dashboard generated: test-interactive-dashboard.html")
        print(f"   File size: {len(interactive_html)} characters")
        
    except Exception as e:
        print(f"❌ Interactive dashboard failed: {e}")
        import traceback
        print(f"   Error details: {traceback.format_exc()}")
    
    try:
        # Test mobile dashboard
        print("\n📱 Testing Mobile Dashboard...")
        from scripts.mobile_responsive_updater import MobileResponsiveUpdater
        
        mobile_generator = MobileResponsiveUpdater(sample_data)
        mobile_html = mobile_generator.generate_mobile_optimized_html()
        
        # Save to file
        with open('test-mobile-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(mobile_html)
        
        print(f"✅ Mobile dashboard generated: test-mobile-dashboard.html")
        print(f"   File size: {len(mobile_html)} characters")
        
    except Exception as e:
        print(f"❌ Mobile dashboard failed: {e}")
        import traceback
        print(f"   Error details: {traceback.format_exc()}")
    
    print("\n" + "=" * 50)
    print("🎯 TEST RESULTS")
    print("=" * 50)
    
    # Check if files were created
    files_created = []
    if os.path.exists('test-interactive-dashboard.html'):
        size = os.path.getsize('test-interactive-dashboard.html')
        files_created.append(f"test-interactive-dashboard.html ({size} bytes)")
    
    if os.path.exists('test-mobile-dashboard.html'):
        size = os.path.getsize('test-mobile-dashboard.html')
        files_created.append(f"test-mobile-dashboard.html ({size} bytes)")
    
    if files_created:
        print("✅ Files created successfully:")
        for file in files_created:
            print(f"   - {file}")
        
        print("\n🌐 To view the dashboards:")
        print("1. Open the HTML files in your web browser")
        print("2. Or use a local server: python -m http.server 8000")
        print("3. Then visit: http://localhost:8000/test-interactive-dashboard.html")
        
    else:
        print("❌ No files were created - check the error messages above")
    
    print("=" * 50)

if __name__ == "__main__":
    test_dashboard_generation()