from collections import deque

class RecentlyViewedTracker:
    def __init__(self, max_recent_views=5):
        self.user_views = {}
        self.max_recent_views = max_recent_views
    
    def track_view(self, user_id: int, article_id: int):
        if user_id not in self.user_views:
            self.user_views[user_id] = deque(maxlen=self.max_recent_views)
        
        # Remove if already exists to avoid duplicates
        if article_id in self.user_views[user_id]:
            self.user_views[user_id].remove(article_id)
        
        self.user_views[user_id].appendleft(article_id)
    
    def get_recent_views(self, user_id: int):
        return list(self.user_views.get(user_id, []))

# Global instance
recent_views_tracker = RecentlyViewedTracker()