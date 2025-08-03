import sys
sys.path.append('scripts')
import run_analytics
import asyncio

if __name__ == "__main__":
    asyncio.run(run_analytics.run_full_pipeline())