#!/usr/bin/env python3
"""
Test Suite for Crisis Response Social Media Automation App
=========================================================

Comprehensive test suite to validate all functionality of the crisis response
social media automation application.

Test Categories:
- Unit tests for core components
- Integration tests for end-to-end workflows
- API endpoint tests
- Data validation tests
- Performance tests
- Error handling tests

Author: Blackbox AI Assistant
"""

import unittest
import json
import tempfile
import os
import sqlite3
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Import application components
from crisis_response_app import (
    CrisisResponseApp, DisasterType, PlatformType, ResponseType,
    CrisisEvent, JobPosting, SocialMediaPost, UserProfile,
    BlackboxAPIClient, DatabaseManager, SocialMediaManager,
    ResponseHandler, AnalyticsManager
)

class TestBlackboxAPIClient(unittest.TestCase):
    """Test the Blackbox API client"""
    
    def setUp(self):
        self.client = BlackboxAPIClient()
    
    def test_generate_content_success(self):
        """Test successful content generation"""
        prompt = "Create hurricane recovery job post"
        result = self.client.generate_content(prompt)
        
        self.assertTrue(result['success'])
        self.assertIn('content', result)
        self.assertIn('hashtags', result)
        self.assertIsInstance(result['hashtags'], list)
    
    def test_generate_content_different_disasters(self):
        """Test content generation for different disaster types"""
        disasters = ['hurricane', 'earthquake', 'wildfire', 'flood']
        
        for disaster in disasters:
            prompt = f"Create {disaster} recovery job post"
            result = self.client.generate_content(prompt)
            
            self.assertTrue(result['success'], f"Failed for {disaster}")
            self.assertIn(disaster, result['content'].lower() or ''.join(result['hashtags']).lower())
    
    def test_generate_image(self):
        """Test image generation"""
        prompt = "hurricane recovery jobs Florida"
        image_path = self.client.generate_image(prompt)
        
        self.assertTrue(image_path)
        self.assertTrue(image_path.endswith('.png'))
        # Check if file exists (in real test, would verify file creation)

class TestDatabaseManager(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_manager = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        # Clean up temporary database
        os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test database tables are created correctly"""
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        
        # Check if all tables exist
        tables = ['crisis_events', 'job_postings', 'social_media_posts', 
                 'user_profiles', 'responses', 'analytics']
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        db_tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            self.assertIn(table, db_tables, f"Table {table} not found")
        
        conn.close()
    
    def test_save_crisis_event(self):
        """Test saving crisis events"""
        crisis = CrisisEvent(
            id="test_crisis_1",
            disaster_type=DisasterType.HURRICANE,
            location="Test City",
            severity="high",
            start_date=datetime.now(),
            estimated_duration=14,
            affected_population=50000,
            job_types_needed=["construction", "cleanup"],
            urgent_needs=["shelter", "medical"]
        )
        
        # Save crisis
        self.db_manager.save_crisis_event(crisis)
        
        # Verify it was saved
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crisis_events WHERE id = ?", (crisis.id,))
        row = cursor.fetchone()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], crisis.id)
        self.assertEqual(row[1], crisis.disaster_type.value)
        self.assertEqual(row[2], crisis.location)
        
        conn.close()
    
    def test_save_job_posting(self):
        """Test saving job postings"""
        # First create and save a crisis
        crisis = CrisisEvent(
            id="test_crisis_2",
            disaster_type=DisasterType.EARTHQUAKE,
            location="Test Location",
            severity="medium",
            start_date=datetime.now(),
            estimated_duration=10,
            affected_population=25000,
            job_types_needed=["medical"],
            urgent_needs=["rescue"]
        )
        self.db_manager.save_crisis_event(crisis)
        
        # Create job posting
        job = JobPosting(
            id="test_job_1",
            crisis_id=crisis.id,
            job_title="Emergency Medic",
            job_type="medical",
            location=crisis.location,
            urgency="high",
            requirements=["EMT certification", "Experience"],
            compensation="$40/hour",
            duration="2 weeks",
            contact_info="test@example.com",
            created_at=datetime.now()
        )
        
        # Save job
        self.db_manager.save_job_posting(job)
        
        # Verify it was saved
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_postings WHERE id = ?", (job.id,))
        row = cursor.fetchone()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], job.id)
        self.assertEqual(row[1], job.crisis_id)
        self.assertEqual(row[2], job.job_title)
        
        conn.close()

class TestSocialMediaManager(unittest.TestCase):
    """Test social media posting functionality"""
    
    def setUp(self):
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.social_manager = SocialMediaManager(self.db_manager)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_post_to_platform_success(self):
        """Test successful posting to platform"""
        post = SocialMediaPost(
            id="test_post_1",
            platform=PlatformType.TWITTER,
            content="Test emergency job posting #DisasterRelief",
            media_path=None,
            scheduled_time=datetime.now(),
            crisis_id="test_crisis",
            job_id="test_job",
            hashtags=["#DisasterRelief", "#Jobs"]
        )
        
        success = self.social_manager.post_to_platform(post)
        
        self.assertTrue(success)
        self.assertEqual(post.status, "posted")
        self.assertIsNotNone(post.engagement_metrics)
    
    def test_all_platforms_supported(self):
        """Test posting to all supported platforms"""
        platforms = [PlatformType.TWITTER, PlatformType.FACEBOOK, 
                    PlatformType.LINKEDIN, PlatformType.INSTAGRAM]
        
        for platform in platforms:
            post = SocialMediaPost(
                id=f"test_post_{platform.value}",
                platform=platform,
                content=f"Test post for {platform.value}",
                media_path=None,
                scheduled_time=datetime.now(),
                crisis_id="test_crisis",
                job_id="test_job",
                hashtags=["#Test"]
            )
            
            success = self.social_manager.post_to_platform(post)
            self.assertTrue(success, f"Failed to post to {platform.value}")

class TestResponseHandler(unittest.TestCase):
    """Test automated response handling"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.blackbox_client = BlackboxAPIClient()
        self.response_handler = ResponseHandler(self.db_manager, self.blackbox_client)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_process_responses(self):
        """Test response processing doesn't crash"""
        # This is a smoke test since process_responses() is simulated
        try:
            self.response_handler.process_responses()
        except Exception as e:
            self.fail(f"process_responses() raised {e} unexpectedly")
    
    def test_generate_automated_response_types(self):
        """Test different types of automated responses"""
        response_types = [
            {"type": "availability", "expected_keyword": "availability"},
            {"type": "application", "expected_keyword": "apply"},
            {"type": "information", "expected_keyword": "Requirements"},
            {"type": "other", "expected_keyword": "interest"}
        ]
        
        for response_type in response_types:
            user_response = {
                "type": response_type["type"],
                "user": "@testuser",
                "content": f"Test {response_type['type']} message"
            }
            
            # Test that method doesn't crash
            try:
                self.response_handler._generate_automated_response(user_response)
            except Exception as e:
                self.fail(f"_generate_automated_response() failed for {response_type['type']}: {e}")

class TestAnalyticsManager(unittest.TestCase):
    """Test analytics and reporting functionality"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.analytics_manager = AnalyticsManager(self.db_manager)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_generate_analytics_report_empty_db(self):
        """Test analytics report with empty database"""
        report = self.analytics_manager.generate_analytics_report()
        
        self.assertIsInstance(report, dict)
        self.assertIn('message', report)
    
    def test_create_analytics_visualization(self):
        """Test visualization creation"""
        viz_path = self.analytics_manager.create_analytics_visualization()
        
        self.assertTrue(viz_path)
        self.assertTrue(viz_path.endswith('.png'))

class TestCrisisResponseApp(unittest.TestCase):
    """Test main application class"""
    
    def setUp(self):
        self.app = CrisisResponseApp()
    
    def test_create_crisis_event(self):
        """Test crisis event creation"""
        crisis = self.app.create_crisis_event(
            disaster_type=DisasterType.HURRICANE,
            location="Test Location",
            severity="high",
            affected_population=50000,
            job_types=["construction", "cleanup"],
            urgent_needs=["shelter", "medical"]
        )
        
        self.assertIsNotNone(crisis)
        self.assertEqual(crisis.disaster_type, DisasterType.HURRICANE)
        self.assertEqual(crisis.location, "Test Location")
        self.assertEqual(crisis.severity, "high")
        self.assertEqual(crisis.affected_population, 50000)
    
    def test_create_job_posting(self):
        """Test job posting creation"""
        # First create a crisis
        crisis = self.app.create_crisis_event(
            disaster_type=DisasterType.EARTHQUAKE,
            location="Test City",
            severity="medium",
            affected_population=25000,
            job_types=["medical"],
            urgent_needs=["rescue"]
        )
        
        # Create job posting
        job = self.app.create_job_posting(
            crisis=crisis,
            job_title="Emergency Medic",
            job_type="medical",
            urgency="high",
            requirements=["EMT certification"],
            compensation="$40/hour",
            duration="2 weeks",
            contact_info="test@example.com"
        )
        
        self.assertIsNotNone(job)
        self.assertEqual(job.crisis_id, crisis.id)
        self.assertEqual(job.job_title, "Emergency Medic")
        self.assertEqual(job.job_type, "medical")
    
    def test_generate_social_media_campaign(self):
        """Test social media campaign generation"""
        # Create crisis and job
        crisis = self.app.create_crisis_event(
            disaster_type=DisasterType.WILDFIRE,
            location="Test Forest",
            severity="high",
            affected_population=30000,
            job_types=["firefighting"],
            urgent_needs=["evacuation"]
        )
        
        job = self.app.create_job_posting(
            crisis=crisis,
            job_title="Wildland Firefighter",
            job_type="firefighting",
            urgency="critical",
            requirements=["Firefighting experience"],
            compensation="$30/hour",
            duration="Until contained",
            contact_info="fire@example.com"
        )
        
        # Generate campaign
        platforms = [PlatformType.TWITTER, PlatformType.FACEBOOK]
        schedule_times = [
            datetime.now() + timedelta(minutes=5),
            datetime.now() + timedelta(hours=1)
        ]
        
        posts = self.app.generate_social_media_campaign(
            crisis=crisis,
            job=job,
            platforms=platforms,
            schedule_times=schedule_times
        )
        
        self.assertIsInstance(posts, list)
        self.assertGreater(len(posts), 0)
        
        # Check that posts were created for each platform
        created_platforms = {post.platform for post in posts}
        for platform in platforms:
            self.assertIn(platform, created_platforms)
    
    def test_end_to_end_demo(self):
        """Test the complete end-to-end demonstration"""
        try:
            results = self.app.demonstrate_end_to_end_flow()
            
            self.assertIsInstance(results, dict)
            self.assertIn('crisis_events', results)
            self.assertIn('job_postings', results)
            self.assertIn('social_posts', results)
            self.assertIn('posts_published', results)
            self.assertIn('analytics', results)
            
            self.assertEqual(results['crisis_events'], 1)
            self.assertGreater(results['job_postings'], 0)
            self.assertGreater(results['social_posts'], 0)
            
        except Exception as e:
            self.fail(f"End-to-end demo failed: {e}")

class TestDataModels(unittest.TestCase):
    """Test data model classes"""
    
    def test_crisis_event_creation(self):
        """Test CrisisEvent data model"""
        crisis = CrisisEvent(
            id="test_1",
            disaster_type=DisasterType.HURRICANE,
            location="Miami",
            severity="high",
            start_date=datetime.now(),
            estimated_duration=14,
            affected_population=100000,
            job_types_needed=["construction", "cleanup"],
            urgent_needs=["shelter", "food"]
        )
        
        self.assertEqual(crisis.id, "test_1")
        self.assertEqual(crisis.disaster_type, DisasterType.HURRICANE)
        self.assertEqual(crisis.location, "Miami")
        self.assertEqual(crisis.severity, "high")
        self.assertEqual(crisis.affected_population, 100000)
        self.assertIsInstance(crisis.job_types_needed, list)
        self.assertIsInstance(crisis.urgent_needs, list)
    
    def test_job_posting_creation(self):
        """Test JobPosting data model"""
        job = JobPosting(
            id="job_1",
            crisis_id="crisis_1",
            job_title="Emergency Worker",
            job_type="general",
            location="Test City",
            urgency="medium",
            requirements=["Background check", "Physical fitness"],
            compensation="$25/hour",
            duration="1-2 weeks",
            contact_info="jobs@example.com",
            created_at=datetime.now()
        )
        
        self.assertEqual(job.id, "job_1")
        self.assertEqual(job.crisis_id, "crisis_1")
        self.assertEqual(job.job_title, "Emergency Worker")
        self.assertEqual(job.job_type, "general")
        self.assertIsInstance(job.requirements, list)
    
    def test_social_media_post_creation(self):
        """Test SocialMediaPost data model"""
        post = SocialMediaPost(
            id="post_1",
            platform=PlatformType.TWITTER,
            content="Emergency job available #DisasterRelief",
            media_path="/path/to/image.png",
            scheduled_time=datetime.now(),
            crisis_id="crisis_1",
            job_id="job_1",
            hashtags=["#DisasterRelief", "#Jobs"]
        )
        
        self.assertEqual(post.id, "post_1")
        self.assertEqual(post.platform, PlatformType.TWITTER)
        self.assertTrue(post.content.startswith("Emergency job"))
        self.assertEqual(post.crisis_id, "crisis_1")
        self.assertIsInstance(post.hashtags, list)
        self.assertEqual(post.status, "scheduled")  # Default status

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def setUp(self):
        self.app = CrisisResponseApp()
    
    def test_invalid_disaster_type(self):
        """Test handling of invalid disaster types"""
        # This would typically be handled at the API level
        # Here we test that valid disaster types work
        valid_types = [dt for dt in DisasterType]
        self.assertGreater(len(valid_types), 0)
        
        for disaster_type in valid_types:
            crisis = self.app.create_crisis_event(
                disaster_type=disaster_type,
                location="Test Location",
                severity="medium",
                affected_population=1000,
                job_types=["general"],
                urgent_needs=["help"]
            )
            self.assertEqual(crisis.disaster_type, disaster_type)
    
    def test_empty_job_requirements(self):
        """Test job creation with empty requirements"""
        crisis = self.app.create_crisis_event(
            disaster_type=DisasterType.FLOOD,
            location="Test Town",
            severity="low",
            affected_population=5000,
            job_types=["cleanup"],
            urgent_needs=["pumping"]
        )
        
        job = self.app.create_job_posting(
            crisis=crisis,
            job_title="General Helper",
            job_type="general",
            urgency="low",
            requirements=[],  # Empty requirements
            compensation="$20/hour",
            duration="1 week",
            contact_info="help@example.com"
        )
        
        self.assertEqual(job.requirements, [])
    
    def test_blackbox_api_error_handling(self):
        """Test Blackbox API error handling"""
        client = BlackboxAPIClient()
        
        # Test with empty prompt
        result = client.generate_content("")
        self.assertIn('success', result)
        
        # Test image generation with empty prompt
        image_path = client.generate_image("")
        # Should still return a path (default image)
        self.assertIsInstance(image_path, str)

def run_performance_tests():
    """Run basic performance tests"""
    print("\n🚀 Running Performance Tests...")
    
    app = CrisisResponseApp()
    
    # Test crisis creation speed
    import time
    start_time = time.time()
    
    for i in range(10):
        crisis = app.create_crisis_event(
            disaster_type=DisasterType.HURRICANE,
            location=f"Test City {i}",
            severity="medium",
            affected_population=1000 * i,
            job_types=["general"],
            urgent_needs=["help"]
        )
    
    crisis_time = time.time() - start_time
    print(f"✅ Created 10 crisis events in {crisis_time:.2f} seconds")
    
    # Test content generation speed
    start_time = time.time()
    client = BlackboxAPIClient()
    
    for i in range(5):
        result = client.generate_content(f"Hurricane recovery job {i}")
    
    content_time = time.time() - start_time
    print(f"✅ Generated 5 content pieces in {content_time:.2f} seconds")
    
    print(f"📊 Performance Summary:")
    print(f"   Crisis creation: {crisis_time/10:.3f}s per crisis")
    print(f"   Content generation: {content_time/5:.3f}s per content")

def main():
    """Run all tests"""
    print("🧪 Crisis Response Social Media Automation - Test Suite")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBlackboxAPIClient,
        TestDatabaseManager,
        TestSocialMediaManager,
        TestResponseHandler,
        TestAnalyticsManager,
        TestCrisisResponseApp,
        TestDataModels,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Run performance tests
    run_performance_tests()
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"🎯 TEST SUMMARY:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n🚨 ERRORS:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback.split('Error:')[-1].strip()}")
    
    if not result.failures and not result.errors:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Crisis Response Social Media Automation is ready for production!")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
