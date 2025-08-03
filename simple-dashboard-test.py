#!/usr/bin/env python3
"""
Simple Dashboard Test
Creates a basic HTML dashboard to test if the issue is with HTML generation or display
"""

import os
from datetime import datetime

def create_simple_dashboard():
    """Create a simple HTML dashboard for testing"""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Analytics Dashboard - Test</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0D1117 0%, #161B22 100%);
            color: #C9D1D9;
            line-height: 1.6;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(22, 27, 34, 0.8);
            border-radius: 15px;
            border: 1px solid rgba(88, 166, 255, 0.2);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(45deg, #58A6FF, #1F6FEB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .card {{
            background: rgba(22, 27, 34, 0.9);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(88, 166, 255, 0.2);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
        
        .card-icon {{
            font-size: 2rem;
            margin-bottom: 15px;
            color: #58A6FF;
        }}
        
        .card-value {{
            font-size: 2.2rem;
            font-weight: bold;
            color: #C9D1D9;
            margin-bottom: 10px;
        }}
        
        .card-label {{
            font-size: 0.9rem;
            color: #8B949E;
            text-transform: uppercase;
        }}
        
        .success-message {{
            background: rgba(46, 160, 67, 0.2);
            color: #2EA043;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
            border: 1px solid rgba(46, 160, 67, 0.3);
        }}
        
        .footer {{
            text-align: center;
            padding: 30px 0;
            color: #8B949E;
            border-top: 1px solid rgba(139, 148, 158, 0.2);
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🚀 GitHub Analytics Dashboard</h1>
            <p>Test Dashboard - HTML Generation Working!</p>
            <p style="font-size: 0.9rem; color: #8B949E; margin-top: 10px;">
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </header>
        
        <div class="success-message">
            <h2>✅ Success!</h2>
            <p>If you can see this dashboard properly formatted with colors and styling, 
               then HTML generation is working correctly!</p>
        </div>
        
        <div class="cards-grid">
            <div class="card">
                <div class="card-icon">📊</div>
                <div class="card-value">25</div>
                <div class="card-label">Repositories</div>
            </div>
            
            <div class="card">
                <div class="card-icon">⭐</div>
                <div class="card-value">150</div>
                <div class="card-label">Total Stars</div>
            </div>
            
            <div class="card">
                <div class="card-icon">🍴</div>
                <div class="card-value">45</div>
                <div class="card-label">Total Forks</div>
            </div>
            
            <div class="card">
                <div class="card-icon">🔥</div>
                <div class="card-value">23 days</div>
                <div class="card-label">Current Streak</div>
            </div>
        </div>
        
        <div style="background: rgba(22, 27, 34, 0.9); border-radius: 12px; padding: 25px; border: 1px solid rgba(88, 166, 255, 0.2);">
            <h3 style="color: #58A6FF; margin-bottom: 15px;">🔍 Troubleshooting Information</h3>
            <p><strong>If you see this dashboard correctly:</strong></p>
            <ul style="margin: 10px 0 10px 20px; color: #8B949E;">
                <li>HTML generation is working fine</li>
                <li>The issue was likely with module imports</li>
                <li>Your browser can display the dashboard properly</li>
            </ul>
            
            <p style="margin-top: 15px;"><strong>If you see raw HTML code instead:</strong></p>
            <ul style="margin: 10px 0 10px 20px; color: #8B949E;">
                <li>The file might be opening in a text editor instead of a browser</li>
                <li>Try right-clicking the HTML file and selecting "Open with" → "Web Browser"</li>
                <li>Or drag the HTML file into your browser window</li>
            </ul>
        </div>
        
        <footer class="footer">
            <p>🧪 Simple Dashboard Test • Generated automatically</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    print("🧪 Creating Simple Dashboard Test")
    print("=" * 50)
    
    try:
        # Generate simple dashboard
        html_content = create_simple_dashboard()
        
        # Save to file
        filename = 'simple-dashboard-test.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        file_size = os.path.getsize(filename)
        
        print(f"✅ Dashboard created successfully!")
        print(f"   File: {filename}")
        print(f"   Size: {file_size} bytes")
        print(f"   Characters: {len(html_content)}")
        
        print("\n🌐 How to view the dashboard:")
        print("1. Double-click the HTML file to open in your default browser")
        print("2. Or right-click → 'Open with' → choose your web browser")
        print("3. Or drag the file into a browser window")
        print("4. Or use: start simple-dashboard-test.html (Windows)")
        
        print("\n🔍 What to look for:")
        print("• If you see a nicely formatted dashboard with dark theme = SUCCESS")
        print("• If you see raw HTML code = the file opened in a text editor")
        print("• If you see the original error from your screenshot = different issue")
        
        # Try to open in browser automatically (Windows)
        try:
            import webbrowser
            webbrowser.open(filename)
            print(f"\n🚀 Attempting to open {filename} in your default browser...")
        except:
            print("\n⚠️ Could not auto-open browser. Please open the file manually.")
        
    except Exception as e:
        print(f"❌ Error creating dashboard: {e}")
        import traceback
        print(f"   Details: {traceback.format_exc()}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()