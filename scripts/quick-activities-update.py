#!/usr/bin/env python3
"""
Quick Current Activities Update Script
For manual updates or testing
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main():
    """Quick update of Current Activities"""
    print("🚀 Quick Current Activities Update")
    print("-" * 40)
    
    try:
        from current_activities_updater import CurrentActivitiesUpdater
        
        username = os.getenv('GITHUB_USERNAME', 'Xenonesis')
        token = os.getenv('GITHUB_TOKEN')
        
        print(f"👤 Username: {username}")
        print(f"🔑 Token: {'✅ Found' if token else '❌ Not found'}")
        
        updater = CurrentActivitiesUpdater(username, token)
        success = await updater.update_readme_current_activities()
        
        if success:
            print("✅ Current Activities updated successfully!")
        else:
            print("❌ Update failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())