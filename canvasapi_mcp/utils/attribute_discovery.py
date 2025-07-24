"""
Semantic attribute discovery and schema mapping for Canvas objects.

This module provides intelligent discovery of Canvas object attributes,
relationship mapping between different object types, and dynamic schema
discovery for unknown Canvas object structures.
"""

import re
import logging
from collections import defaultdict
from canvasapi_get.canvas_object import CanvasObject

logger = logging.getLogger(__name__)


class AttributeDiscovery:
    """
    Discovers and maps Canvas object attributes with semantic understanding.
    
    Provides functionality for:
    - Semantic attribute categorization
    - Relationship mapping between Canvas objects
    - Dynamic schema discovery for unknown object types
    - Attribute importance scoring for DataFrame optimization
    """
    
    def __init__(self):
        """Initialize the attribute discovery system."""
        self._attribute_cache = {}
        self._relationship_cache = {}
        self._schema_cache = {}
        
        # Semantic attribute categories
        self.attribute_categories = {
            'identifiers': [
                'id', 'uuid', 'sis_user_id', 'sis_course_id', 'sis_account_id', 
                'sis_section_id', 'integration_id', 'lti_user_id', 'course_code',
                'account_id', 'user_id', 'group_id', 'section_id', 'enrollment_id'
            ],
            'names_titles': [
                'name', 'title', 'display_name', 'short_name', 'full_name',
                'course_name', 'account_name', 'sortable_name', 'login_id'
            ],
            'descriptions': [
                'description', 'syllabus_body', 'body', 'message', 'instructions',
                'public_description', 'conclusion'
            ],
            'timestamps': [
                'created_at', 'updated_at', 'deleted_at', 'due_at', 'unlock_at',
                'lock_at', 'start_at', 'end_at', 'posted_at', 'graded_at',
                'submitted_at', 'last_activity_at'
            ],
            'status_flags': [
                'published', 'active', 'deleted', 'hidden', 'locked', 'completed',
                'available', 'visible', 'workflow_state', 'enrollment_state'
            ],
            'numerical_data': [
                'points_possible', 'score', 'grade', 'position', 'points',
                'size', 'submission_count', 'graded_count', 'course_count'
            ],
            'urls_links': [
                'url', 'html_url', 'preview_url', 'download_url', 'avatar_url',
                'thumbnail_url', 'alternate_url'
            ],
            'permissions': [
                'permissions', 'can_edit', 'can_delete', 'can_update', 'can_view',
                'readable', 'writable'
            ]
        }
        
        # Canvas object relationship patterns
        self.relationship_patterns = {
            'course': ['account_id', 'enrollment_term_id', 'root_account_id'],
            'user': ['account_id', 'root_account_id'],
            'assignment': ['course_id', 'assignment_group_id', 'quiz_id'],
            'submission': ['assignment_id', 'user_id', 'course_id'],
            'enrollment': ['course_id', 'user_id', 'section_id', 'role_id'],
            'discussion_topic': ['course_id', 'assignment_id', 'group_category_id'],
            'quiz': ['course_id', 'assignment_id', 'assignment_group_id'],
            'module': ['course_id'],
            'page': ['course_id'],
            'file': ['folder_id', 'user_id', 'course_id'],
            'folder': ['parent_folder_id', 'course_id'],
            'group': ['group_category_id', 'account_id', 'course_id'],
            'section': ['course_id', 'account_id']
        }
    
    def discover_attributes(
        self, 
        obj: CanvasObject | type | list[CanvasObject], 
        include_relationships: bool = True
    ) -> dict:
        """
        Discover and categorize attributes of Canvas objects.
        
        Args:
            obj: Canvas object, class, or list of objects to analyze
            include_relationships: Whether to include relationship mapping
            
        Returns:
            Dictionary containing discovered attribute information
        """
        if isinstance(obj, list):
            if not obj:
                return {'attributes': [], 'categories': {}, 'relationships': {}}
            # Analyze first object as representative sample
            obj = obj[0]
        
        obj_type = type(obj).__name__.lower() if hasattr(obj, '__dict__') else str(obj).lower()
        
        # Check cache first
        cache_key = f"{obj_type}_attrs"
        if cache_key in self._attribute_cache:
            return self._attribute_cache[cache_key]
        
        try:
            attributes = []
            
            if hasattr(obj, '__dict__'):
                # Get attributes from instance
                attributes = [attr for attr in obj.__dict__.keys() if not attr.startswith('_')]
            elif hasattr(obj, '__annotations__'):
                # Get attributes from class annotations
                attributes = list(obj.__annotations__.keys())
            else:
                # Fallback to dir() filtering
                attributes = [attr for attr in dir(obj) if not attr.startswith('_') and not callable(getattr(obj, attr, None))]
            
            # Categorize attributes
            categorized = self._categorize_attributes(attributes)
            
            # Discover relationships
            relationships = {}
            if include_relationships:
                relationships = self._discover_relationships(obj_type, attributes)
            
            # Calculate attribute importance
            importance_scores = self._calculate_importance_scores(attributes, obj_type)
            
            result = {
                'object_type': obj_type,
                'attributes': attributes,
                'categories': categorized,
                'relationships': relationships,
                'importance_scores': importance_scores,
                'total_attributes': len(attributes)
            }
            
            # Cache the result
            self._attribute_cache[cache_key] = result
            return result
            
        except Exception as e:
            logger.error(f"Attribute discovery failed for {obj_type}: {str(e)}")
            return {
                'object_type': obj_type,
                'attributes': [],
                'categories': {},
                'relationships': {},
                'importance_scores': {},
                'error': str(e)
            }
    
    def _categorize_attributes(self, attributes: list[str]) -> dict[str, list[str]]:
        """Categorize attributes by semantic meaning."""
        categorized = defaultdict(list)
        uncategorized = []
        
        for attr in attributes:
            attr_lower = attr.lower()
            found_category = False
            
            for category, patterns in self.attribute_categories.items():
                for pattern in patterns:
                    if (pattern == attr_lower or 
                        pattern in attr_lower or 
                        attr_lower.endswith(pattern) or
                        attr_lower.startswith(pattern)):
                        categorized[category].append(attr)
                        found_category = True
                        break
                if found_category:
                    break
            
            if not found_category:
                uncategorized.append(attr)
        
        # Add uncategorized items
        if uncategorized:
            categorized['other'] = uncategorized
        
        return dict(categorized)
    
    def _discover_relationships(self, object_type: str, attributes: list[str]) -> dict:
        """Discover relationship patterns in Canvas object attributes."""
        relationships = {
            'parent_objects': [],
            'child_references': [],
            'many_to_many': [],
            'foreign_keys': []
        }
        
        # Check known relationship patterns
        if object_type in self.relationship_patterns:
            known_relations = self.relationship_patterns[object_type]
            for attr in attributes:
                if attr in known_relations:
                    relationships['foreign_keys'].append({
                        'attribute': attr,
                        'references': self._infer_referenced_object(attr),
                        'relationship_type': 'many_to_one'
                    })
        
        # Discover parent-child relationships
        for attr in attributes:
            attr_lower = attr.lower()
            
            # Parent object indicators
            if any(pattern in attr_lower for pattern in ['parent_', 'root_', 'account_']):
                relationships['parent_objects'].append(attr)
            
            # Child reference indicators (arrays/lists)
            elif any(pattern in attr_lower for pattern in ['_ids', '_list', 'children']):
                relationships['child_references'].append(attr)
            
            # Many-to-many indicators
            elif any(pattern in attr_lower for pattern in ['tags', 'groups', 'members']):
                relationships['many_to_many'].append(attr)
        
        return relationships
    
    def _infer_referenced_object(self, attribute_name: str) -> str | None:
        """Infer the referenced object type from attribute name."""
        attr_lower = attribute_name.lower()
        
        # Common Canvas object reference patterns
        reference_patterns = {
            'course_id': 'course',
            'user_id': 'user', 
            'account_id': 'account',
            'assignment_id': 'assignment',
            'section_id': 'section',
            'group_id': 'group',
            'enrollment_id': 'enrollment',
            'quiz_id': 'quiz',
            'discussion_id': 'discussion_topic',
            'file_id': 'file',
            'folder_id': 'folder',
            'module_id': 'module',
            'page_id': 'page'
        }
        
        for pattern, object_type in reference_patterns.items():
            if pattern in attr_lower:
                return object_type
        
        # Generic pattern: remove _id suffix
        if attr_lower.endswith('_id'):
            return attr_lower[:-3]
        
        return None
    
    def _calculate_importance_scores(self, attributes: list[str], object_type: str) -> dict[str, float]:
        """Calculate importance scores for attributes in DataFrame context."""
        scores = {}
        
        for attr in attributes:
            score = 1.0  # Base score
            attr_lower = attr.lower()
            
            # High importance for identifiers
            if any(pattern in attr_lower for pattern in ['id', 'uuid']):
                score += 2.0
            
            # High importance for names and titles
            if any(pattern in attr_lower for pattern in ['name', 'title']):
                score += 1.5
            
            # Medium importance for status and workflow
            if any(pattern in attr_lower for pattern in ['state', 'status', 'published', 'active']):
                score += 1.0
            
            # Medium importance for timestamps
            if any(pattern in attr_lower for pattern in ['_at', 'date', 'time']):
                score += 0.8
            
            # Lower importance for large text fields
            if any(pattern in attr_lower for pattern in ['description', 'body', 'syllabus']):
                score += 0.3
            
            # Lower importance for URLs
            if any(pattern in attr_lower for pattern in ['url', 'link']):
                score += 0.5
            
            scores[attr] = score
        
        return scores
    
    def get_core_attributes(
        self, 
        object_type: str, 
        max_attributes: int = 20
    ) -> list[str]:
        """
        Get core attributes for an object type suitable for DataFrame display.
        
        Args:
            object_type: Canvas object type
            max_attributes: Maximum number of attributes to return
            
        Returns:
            List of core attribute names ordered by importance
        """
        cache_key = f"{object_type}_core_{max_attributes}"
        if cache_key in self._schema_cache:
            return self._schema_cache[cache_key]
        
        # Define core attributes for common Canvas objects
        core_attribute_sets = {
            'course': [
                'id', 'name', 'course_code', 'workflow_state', 'account_id',
                'enrollment_term_id', 'created_at', 'updated_at', 'start_at', 'end_at'
            ],
            'user': [
                'id', 'name', 'email', 'login_id', 'sis_user_id', 'workflow_state',
                'created_at', 'updated_at', 'last_activity_at'
            ],
            'assignment': [
                'id', 'name', 'description', 'course_id', 'points_possible',
                'due_at', 'unlock_at', 'lock_at', 'published', 'workflow_state'
            ],
            'enrollment': [
                'id', 'user_id', 'course_id', 'section_id', 'type', 'enrollment_state',
                'created_at', 'updated_at', 'role', 'role_id'
            ],
            'submission': [
                'id', 'assignment_id', 'user_id', 'submitted_at', 'score', 'grade',
                'workflow_state', 'submission_type', 'attempt'
            ]
        }
        
        core_attrs = core_attribute_sets.get(object_type, [])
        
        # If we have fewer core attributes than requested, we'll need discovery
        if len(core_attrs) < max_attributes:
            # This would require an object instance for full discovery
            # For now, return what we have
            pass
        
        result = core_attrs[:max_attributes]
        self._schema_cache[cache_key] = result
        return result
    
    def discover_object_schema(
        self, 
        objects: list[CanvasObject],
        sample_size: int = 100
    ) -> dict:
        """
        Discover comprehensive schema from a list of Canvas objects.
        
        Args:
            objects: List of Canvas objects to analyze
            sample_size: Number of objects to sample for analysis
            
        Returns:
            Dictionary containing discovered schema information
        """
        if not objects:
            return {'schema': {}, 'statistics': {}}
        
        # Sample objects for analysis
        sample = objects[:min(sample_size, len(objects))]
        object_type = type(sample[0]).__name__.lower()
        
        # Collect all attributes and their occurrence frequency
        attribute_stats = defaultdict(lambda: {'count': 0, 'types': set(), 'samples': []})
        
        for obj in sample:
            for attr_name, attr_value in obj.__dict__.items():
                if attr_name.startswith('_'):
                    continue
                
                stats = attribute_stats[attr_name]
                stats['count'] += 1
                stats['types'].add(type(attr_value).__name__)
                
                # Store sample values (first 3)
                if len(stats['samples']) < 3:
                    stats['samples'].append(attr_value)
        
        # Calculate attribute statistics
        total_objects = len(sample)
        schema = {}
        
        for attr_name, stats in attribute_stats.items():
            schema[attr_name] = {
                'frequency': stats['count'] / total_objects,
                'types': list(stats['types']),
                'primary_type': max(stats['types'], key=lambda t: str(stats['types']).count(t)),
                'samples': stats['samples'][:3],
                'is_consistent': len(stats['types']) == 1,
                'coverage': stats['count'] / total_objects
            }
        
        # Overall statistics
        statistics = {
            'total_objects_analyzed': total_objects,
            'unique_attributes': len(schema),
            'object_type': object_type,
            'most_common_attributes': sorted(
                schema.keys(), 
                key=lambda attr: schema[attr]['frequency'], 
                reverse=True
            )[:10],
            'coverage_distribution': {
                'high_coverage': len([a for a in schema.values() if a['coverage'] > 0.9]),
                'medium_coverage': len([a for a in schema.values() if 0.5 < a['coverage'] <= 0.9]),
                'low_coverage': len([a for a in schema.values() if a['coverage'] <= 0.5])
            }
        }
        
        return {
            'schema': schema,
            'statistics': statistics,
            'object_type': object_type
        }
    
    def suggest_dataframe_columns(
        self, 
        schema_info: dict,
        max_columns: int = 30,
        min_coverage: float = 0.1
    ) -> list[str]:
        """
        Suggest optimal columns for DataFrame representation.
        
        Args:
            schema_info: Schema information from discover_object_schema
            max_columns: Maximum number of columns to suggest
            min_coverage: Minimum attribute coverage to include
            
        Returns:
            List of suggested column names
        """
        if 'schema' not in schema_info:
            return []
        
        schema = schema_info['schema']
        
        # Filter attributes by coverage and consistency
        candidates = []
        for attr_name, attr_info in schema.items():
            if attr_info['coverage'] >= min_coverage:
                # Calculate suggestion score
                score = attr_info['coverage']
                
                # Bonus for consistent types
                if attr_info['is_consistent']:
                    score += 0.2
                
                # Bonus for important attribute types
                if any(pattern in attr_name.lower() for pattern in ['id', 'name', 'title']):
                    score += 0.3
                
                # Penalty for complex types
                if 'dict' in attr_info['types'] or 'list' in attr_info['types']:
                    score -= 0.1
                
                candidates.append((attr_name, score))
        
        # Sort by score and return top candidates
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [attr_name for attr_name, _ in candidates[:max_columns]]
    
    def map_object_relationships(
        self, 
        objects: list[CanvasObject]
    ) -> dict[str, list[dict]]:
        """
        Map relationships between Canvas objects.
        
        Args:
            objects: List of Canvas objects to analyze
            
        Returns:
            Dictionary mapping relationship types to relationship information
        """
        if not objects:
            return {}
        
        object_type = type(objects[0]).__name__.lower()
        relationships = defaultdict(list)
        
        # Analyze first few objects for relationship patterns
        sample = objects[:min(50, len(objects))]
        
        for obj in sample:
            for attr_name, attr_value in obj.__dict__.items():
                if attr_name.startswith('_'):
                    continue
                
                # Check for foreign key patterns
                if attr_name.lower().endswith('_id') and attr_value is not None:
                    referenced_type = self._infer_referenced_object(attr_name)
                    if referenced_type:
                        relationships['foreign_keys'].append({
                            'attribute': attr_name,
                            'references': referenced_type,
                            'sample_value': attr_value
                        })
                
                # Check for nested Canvas objects
                elif isinstance(attr_value, CanvasObject):
                    relationships['nested_objects'].append({
                        'attribute': attr_name,
                        'object_type': type(attr_value).__name__.lower(),
                        'relationship': 'composition'
                    })
                
                # Check for lists of Canvas objects
                elif isinstance(attr_value, list) and attr_value and isinstance(attr_value[0], CanvasObject):
                    relationships['object_collections'].append({
                        'attribute': attr_name,
                        'object_type': type(attr_value[0]).__name__.lower(),
                        'relationship': 'one_to_many',
                        'collection_size': len(attr_value)
                    })
        
        # Remove duplicates
        for rel_type, rel_list in relationships.items():
            seen = set()
            unique_relationships = []
            for rel in rel_list:
                key = (rel['attribute'], rel.get('references', rel.get('object_type')))
                if key not in seen:
                    seen.add(key)
                    unique_relationships.append(rel)
            relationships[rel_type] = unique_relationships
        
        return dict(relationships)
    
    def clear_caches(self):
        """Clear all internal caches."""
        self._attribute_cache.clear()
        self._relationship_cache.clear()  
        self._schema_cache.clear()
        logger.info("Attribute discovery caches cleared")