"""
Database Router for Multi-Database Architecture

This router directs database operations to the appropriate database:
- MySQL (default): User data, courses, enrollments, and relational data
- MongoDB: Analytics, logs, user behavior, and document-oriented data

Usage:
    Add to settings.py:
    DATABASE_ROUTERS = ['courseproject.db_routers.DatabaseRouter']
"""


class DatabaseRouter:
    """
    A router to control all database operations on models across
    multiple databases (MySQL and MongoDB).
    
    Simplified to use app-based routing only for cleaner maintenance.
    All models in the 'analytics' app go to MongoDB, everything else to MySQL.
    """
    
    # Apps that should use MongoDB (cleaner than tracking individual models)
    MONGO_APP_LABELS = {'analytics'}
    
    def _is_mongo_model(self, model):
        """
        Check if a model should use MongoDB based on app label only.
        Simpler and easier to maintain than tracking individual models.
        """
        return model._meta.app_label in self.MONGO_APP_LABELS
    
    def db_for_read(self, model, **hints):
        """
        Route MongoDB app models to 'mongodb', all others to 'default' (MySQL).
        """
        if self._is_mongo_model(model):
            return 'mongodb'
        return 'default'
    
    def db_for_write(self, model, **hints):
        """
        Route MongoDB app models to 'mongodb', all others to 'default' (MySQL).
        """
        if self._is_mongo_model(model):
            return 'mongodb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database.
        
        Cross-database relations are not allowed to maintain data integrity.
        If you need to reference data across databases, use explicit
        foreign keys stored as integers/strings rather than ForeignKey fields.
        """
        db1 = 'mongodb' if self._is_mongo_model(obj1.__class__) else 'default'
        db2 = 'mongodb' if self._is_mongo_model(obj2.__class__) else 'default'
        return db1 == db2
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure migrations go to the correct database based on app label.
        """
        if app_label in self.MONGO_APP_LABELS:
            return db == 'mongodb'
        return db == 'default'


class PrimaryReplicaRouter:
    """
    A router that implements primary/replica routing for read scaling.
    
    This is an advanced router for high-traffic applications that need
    to distribute read queries across multiple database replicas.
    
    Usage (add both routers):
    DATABASE_ROUTERS = [
        'courseproject.db_routers.DatabaseRouter',
        'courseproject.db_routers.PrimaryReplicaRouter',
    ]
    
    Configure databases:
    DATABASES = {
        'default': {...},           # Primary (read/write)
        'replica': {...},           # Read replica
        'mongodb': {...},           # Document store
    }
    """
    
    def db_for_read(self, model, **hints):
        """
        Route reads to the replica database for load balancing.
        
        Note: This only handles MySQL models. MongoDB routing is
        handled by DatabaseRouter which runs first.
        """
        # Skip if this is a MongoDB model (handled by DatabaseRouter)
        if hasattr(model, '_meta') and model._meta.app_label == 'analytics':
            return None
        
        # Use replica for reads if available
        # Uncomment when you add a replica database
        # return 'replica'
        return None
    
    def db_for_write(self, model, **hints):
        """
        All writes go to the primary database.
        """
        return None  # Use default behavior
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations are allowed between objects in the MySQL cluster.
        """
        # Both primary and replica are the same logical database
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Migrations should only run on the primary database.
        """
        # Only allow migrations on the primary (default) database
        if db == 'replica':
            return False
        return None
