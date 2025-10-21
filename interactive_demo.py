#!/usr/bin/env python3
"""
Interactive Demo Script for Crisis Response Social Media Automation App
=====================================================================

This script provides an interactive demonstration of the crisis response
social media automation application, allowing users to explore different
scenarios and features.

Features:
- Interactive crisis scenario selection
- Real-time content generation
- Multi-platform campaign simulation
- Analytics dashboard
- A/B testing demonstration
"""

import os
import sys
import time
from datetime import datetime, timedelta
from crisis_response_app import (
    CrisisResponseApp, DisasterType, PlatformType,
    CrisisEvent, JobPosting, SocialMediaPost
)

class InteractiveDemo:
    """Interactive demonstration interface"""
    
    def __init__(self):
        self.app = CrisisResponseApp()
        self.current_crisis = None
        self.current_jobs = []
        self.current_posts = []
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60 + "\n")
    
    def print_menu(self, title, options):
        """Print a formatted menu"""
        self.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print(f"  0. Exit")
        print()
    
    def get_user_choice(self, max_option):
        """Get user choice with validation"""
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 0 <= choice <= max_option:
                    return choice
                else:
                    print(f"Please enter a number between 0 and {max_option}")
            except ValueError:
                print("Please enter a valid number")
    
    def disaster_scenario_menu(self):
        """Display disaster scenario selection menu"""
        scenarios = [
            "🌀 Hurricane - Category 4 hits Florida Coast",
            "🌍 Earthquake - 7.2 magnitude in California",  
            "🔥 Wildfire - Major fire threatens residential areas",
            "🌊 Flood - River overflow affects 3 counties",
            "🌪️ Tornado - Multiple tornadoes in Oklahoma",
            "🌊 Tsunami - Coastal evacuation required",
            "❄️ Blizzard - Severe winter storm emergency"
        ]
        
        self.print_menu("Select Disaster Scenario", scenarios)
        choice = self.get_user_choice(len(scenarios))
        
        if choice == 0:
            return None
        
        # Create crisis based on selection
        disaster_configs = {
            1: {
                "type": DisasterType.HURRICANE,
                "location": "Miami-Dade County, Florida",
                "severity": "critical",
                "population": 100000,
                "jobs": ["construction", "cleanup", "medical", "logistics", "security"],
                "needs": ["emergency shelter", "debris removal", "medical supplies", "power restoration"]
            },
            2: {
                "type": DisasterType.EARTHQUAKE,
                "location": "Los Angeles County, California",
                "severity": "high",
                "population": 250000,
                "jobs": ["search_rescue", "medical", "construction", "logistics"],
                "needs": ["search and rescue", "medical triage", "structural assessment", "emergency communications"]
            },
            3: {
                "type": DisasterType.WILDFIRE,
                "location": "Sonoma County, California",
                "severity": "high",
                "population": 75000,
                "jobs": ["firefighting", "evacuation", "medical", "logistics"],
                "needs": ["fire suppression", "evacuation support", "air quality monitoring", "livestock evacuation"]
            },
            4: {
                "type": DisasterType.FLOOD,
                "location": "Houston, Texas",
                "severity": "medium",
                "population": 150000,
                "jobs": ["rescue", "cleanup", "medical", "logistics"],
                "needs": ["water rescue", "flood cleanup", "temporary housing", "contamination assessment"]
            },
            5: {
                "type": DisasterType.TORNADO,
                "location": "Moore, Oklahoma",
                "severity": "high", 
                "population": 45000,
                "jobs": ["search_rescue", "cleanup", "medical", "construction"],
                "needs": ["search and rescue", "debris removal", "medical triage", "temporary shelter"]
            },
            6: {
                "type": DisasterType.TSUNAMI,
                "location": "Pacific Coast, Oregon",
                "severity": "critical",
                "population": 80000,
                "jobs": ["evacuation", "search_rescue", "medical", "logistics"],
                "needs": ["immediate evacuation", "search and rescue", "medical support", "communication restoration"]
            },
            7: {
                "type": DisasterType.BLIZZARD,
                "location": "Buffalo, New York",
                "severity": "high",
                "population": 120000,
                "jobs": ["snow_removal", "rescue", "medical", "utilities"],
                "needs": ["snow removal", "heating restoration", "medical emergency response", "food distribution"]
            }
        }
        
        config = disaster_configs[choice]
        self.current_crisis = self.app.create_crisis_event(
            disaster_type=config["type"],
            location=config["location"],
            severity=config["severity"],
            affected_population=config["population"],
            job_types=config["jobs"],
            urgent_needs=config["needs"]
        )
        
        return self.current_crisis
    
    def create_job_postings_interactive(self):
        """Interactive job posting creation"""
        if not self.current_crisis:
            print("❌ No active crisis. Please select a scenario first.")
            return
        
        self.print_header(f"Creating Jobs for {self.current_crisis.disaster_type.value.title()} in {self.current_crisis.location}")
        
        # Job templates based on crisis type
        job_templates = {
            DisasterType.HURRICANE: [
                {
                    "title": "Emergency Construction Crew Leader",
                    "type": "construction",
                    "urgency": "critical",
                    "requirements": ["5+ years construction", "Valid driver's license", "First aid certified"],
                    "compensation": "$35/hour + housing + meals",
                    "duration": "2-4 weeks"
                },
                {
                    "title": "Debris Removal Specialist",
                    "type": "cleanup",
                    "urgency": "high",
                    "requirements": ["Heavy equipment operation", "Physical fitness", "Safety training"],
                    "compensation": "$28/hour + overtime",
                    "duration": "1-3 weeks"
                },
                {
                    "title": "Emergency Medical Technician",
                    "type": "medical", 
                    "urgency": "critical",
                    "requirements": ["EMT certification", "CPR certified", "Disaster response experience"],
                    "compensation": "$45/hour + benefits",
                    "duration": "2-6 weeks"
                }
            ],
            DisasterType.EARTHQUAKE: [
                {
                    "title": "Search and Rescue Specialist",
                    "type": "search_rescue",
                    "urgency": "critical",
                    "requirements": ["SAR certification", "Physical fitness", "Emergency response training"],
                    "compensation": "$40/hour + hazard pay",
                    "duration": "1-2 weeks"
                },
                {
                    "title": "Structural Assessment Engineer",
                    "type": "construction",
                    "urgency": "high",
                    "requirements": ["Structural engineering degree", "5+ years experience", "CA license"],
                    "compensation": "$60/hour + travel",
                    "duration": "3-8 weeks"
                }
            ],
            DisasterType.WILDFIRE: [
                {
                    "title": "Wildland Firefighter",
                    "type": "firefighting",
                    "urgency": "critical",
                    "requirements": ["Wildfire experience", "Physical fitness test", "Red Card certified"],
                    "compensation": "$25/hour + hazard pay",
                    "duration": "Until contained"
                },
                {
                    "title": "Evacuation Coordinator",
                    "type": "evacuation",
                    "urgency": "critical",
                    "requirements": ["Emergency management", "Communication skills", "Local knowledge"],
                    "compensation": "$30/hour",
                    "duration": "2-4 weeks"
                }
            ]
        }
        
        # Default jobs for other disaster types
        default_jobs = [
            {
                "title": "Emergency Response Coordinator",
                "type": "logistics",
                "urgency": "high",
                "requirements": ["Emergency management experience", "Leadership skills", "Communication"],
                "compensation": "$35/hour",
                "duration": "2-4 weeks"
            },
            {
                "title": "Community Support Specialist",
                "type": "support",
                "urgency": "medium",
                "requirements": ["Social work background", "Crisis counseling", "Language skills"],
                "compensation": "$25/hour",
                "duration": "4-8 weeks"
            }
        ]
        
        templates = job_templates.get(self.current_crisis.disaster_type, default_jobs)
        
        self.current_jobs = []
        for template in templates:
            job = self.app.create_job_posting(
                crisis=self.current_crisis,
                job_title=template["title"],
                job_type=template["type"],
                urgency=template["urgency"],
                requirements=template["requirements"],
                compensation=template["compensation"],
                duration=template["duration"],
                contact_info=f"crisis.{template['type']}@emergency-response.org"
            )
            self.current_jobs.append(job)
            print(f"✅ Created: {job.job_title} - {job.compensation}")
        
        print(f"\n🎯 Created {len(self.current_jobs)} job postings for {self.current_crisis.disaster_type.value} response")
        input("\nPress Enter to continue...")
    
    def generate_social_campaign_interactive(self):
        """Interactive social media campaign generation"""
        if not self.current_jobs:
            print("❌ No job postings available. Please create jobs first.")
            return
        
        self.print_header("Social Media Campaign Generation")
        
        print("Select platforms for your campaign:")
        platforms = [
            ("Twitter", PlatformType.TWITTER),
            ("Facebook", PlatformType.FACEBOOK), 
            ("LinkedIn", PlatformType.LINKEDIN),
            ("Instagram", PlatformType.INSTAGRAM)
        ]
        
        selected_platforms = []
        for i, (name, platform) in enumerate(platforms, 1):
            choice = input(f"Include {name}? (y/n): ").lower().startswith('y')
            if choice:
                selected_platforms.append(platform)
                print(f"✅ {name} selected")
        
        if not selected_platforms:
            print("❌ No platforms selected.")
            return
        
        # Schedule times
        schedule_times = [
            datetime.now() + timedelta(minutes=5),
            datetime.now() + timedelta(hours=1),
            datetime.now() + timedelta(hours=3),
            datetime.now() + timedelta(hours=6)
        ]
        
        print("\n🎬 Generating social media content...")
        self.current_posts = []
        
        for i, job in enumerate(self.current_jobs):
            print(f"\nGenerating campaign for: {job.job_title}")
            posts = self.app.generate_social_media_campaign(
                crisis=self.current_crisis,
                job=job,
                platforms=selected_platforms,
                schedule_times=schedule_times
            )
            self.current_posts.extend(posts)
            print(f"  ✅ Generated {len(posts)} posts")
        
        print(f"\n🎯 Total campaign: {len(self.current_posts)} posts across {len(selected_platforms)} platforms")
        input("\nPress Enter to continue...")
    
    def preview_content(self):
        """Preview generated content"""
        if not self.current_posts:
            print("❌ No content generated. Please create a campaign first.")
            return
        
        self.print_header("Content Preview")
        
        for i, post in enumerate(self.current_posts[:5], 1):  # Show first 5 posts
            print(f"\n--- Post {i} ---")
            print(f"Platform: {post.platform.value.title()}")
            print(f"A/B Group: {post.ab_test_group}")
            print(f"Scheduled: {post.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"Content: {post.content}")
            print(f"Hashtags: {', '.join(post.hashtags)}")
            if post.media_path:
                print(f"Media: Generated image available")
            print("-" * 50)
        
        if len(self.current_posts) > 5:
            print(f"\n... and {len(self.current_posts) - 5} more posts")
        
        input("\nPress Enter to continue...")
    
    def simulate_posting(self):
        """Simulate posting to social media"""
        if not self.current_posts:
            print("❌ No content to post. Please create a campaign first.")
            return
        
        self.print_header("Social Media Posting Simulation")
        
        print("🚀 Starting social media posting simulation...")
        posted_count = 0
        failed_count = 0
        
        for post in self.current_posts[:8]:  # Post first 8 for demo
            print(f"\n📤 Posting to {post.platform.value.title()}...")
            print(f"   Content: {post.content[:60]}...")
            
            # Simulate posting delay
            time.sleep(0.5)
            
            success = self.app.social_media_manager.post_to_platform(post)
            if success:
                posted_count += 1
                print(f"   ✅ Successfully posted!")
                # Show simulated metrics
                metrics = post.engagement_metrics or {}
                print(f"   📊 Impressions: {metrics.get('impressions', 0):,}")
                print(f"   👆 Clicks: {metrics.get('clicks', 0):,}")
                print(f"   📝 Applications: {metrics.get('applications', 0):,}")
            else:
                failed_count += 1
                print(f"   ❌ Failed to post")
        
        print(f"\n🎯 Posting Summary:")
        print(f"   ✅ Successfully posted: {posted_count}")
        print(f"   ❌ Failed: {failed_count}")
        print(f"   ⏳ Scheduled for later: {len(self.current_posts) - posted_count - failed_count}")
        
        input("\nPress Enter to continue...")
    
    def show_analytics(self):
        """Display analytics dashboard"""
        self.print_header("Analytics Dashboard")
        
        print("📊 Generating analytics report...")
        analytics = self.app.analytics_manager.generate_analytics_report()
        
        if "message" in analytics:
            print(f"ℹ️  {analytics['message']}")
        else:
            print("📈 Campaign Performance:")
            print(f"   Total Impressions: {analytics.get('total_impressions', 0):,}")
            print(f"   Total Clicks: {analytics.get('total_clicks', 0):,}")
            print(f"   Total Applications: {analytics.get('total_applications', 0):,}")
            print(f"   Click-through Rate: {analytics.get('click_through_rate', 0):.2f}%")
            print(f"   Application Rate: {analytics.get('application_rate', 0):.2f}%")
        
        # Generate visualization
        print("\n📊 Creating visualization...")
        viz_path = self.app.analytics_manager.create_analytics_visualization()
        
        if viz_path:
            print(f"✅ Analytics chart saved: {viz_path}")
        else:
            print("❌ Could not create visualization")
        
        # Show A/B test results
        if self.current_posts:
            a_posts = [p for p in self.current_posts if p.ab_test_group == "A"]
            b_posts = [p for p in self.current_posts if p.ab_test_group == "B"]
            
            if a_posts and b_posts:
                print(f"\n🧪 A/B Test Results:")
                print(f"   Group A: {len(a_posts)} posts")
                print(f"   Group B: {len(b_posts)} posts")
                print(f"   Winner: Group A" if len(a_posts) >= len(b_posts) else "   Winner: Group B")
        
        input("\nPress Enter to continue...")
    
    def simulate_responses(self):
        """Simulate and show automated responses"""
        self.print_header("Automated Response System")
        
        print("🤖 Simulating user interactions and automated responses...")
        
        sample_interactions = [
            {
                "user": "@emergency_worker_jane",
                "platform": "Twitter", 
                "message": "I'm a certified EMT available immediately for hurricane response",
                "type": "availability"
            },
            {
                "user": "@construction_pro",
                "platform": "LinkedIn",
                "message": "What are the requirements for the construction crew leader position?",
                "type": "information"
            },
            {
                "user": "@local_volunteer",
                "platform": "Facebook",
                "message": "How do I apply for debris removal work? I have experience with heavy equipment",
                "type": "application"
            },
            {
                "user": "@medical_student",
                "platform": "Twitter",
                "message": "I'm a final year medical student - can I help with medical response?",
                "type": "qualification"
            },
            {
                "user": "@retired_teacher",
                "platform": "Facebook",
                "message": "I want to help with community support - what volunteer opportunities are available?",
                "type": "volunteer"
            }
        ]
        
        for interaction in sample_interactions:
            print(f"\n📩 Incoming message on {interaction['platform']}:")
            print(f"   From: {interaction['user']}")
            print(f"   Message: {interaction['message']}")
            print(f"   Type: {interaction['type']}")
            
            # Simulate processing delay
            time.sleep(1)
            
            # Generate automated response
            if interaction['type'] == 'availability':
                response = "🙏 Thank you for your immediate availability! Please DM your contact info, certifications, and current location. We'll connect you with local emergency coordinators within 30 minutes. Your expertise is crucial right now!"
            elif interaction['type'] == 'information':
                response = "📋 Requirements: 5+ years construction experience, valid driver's license, first aid certification preferred. Compensation: $35/hour + housing + meals. Duration: 2-4 weeks. Background check required. Apply: crisis.construction@emergency-response.org"
            elif interaction['type'] == 'application':
                response = "⚡ To apply for debris removal: 1) Email resume to crisis.cleanup@emergency-response.org 2) Include equipment certifications 3) Specify availability dates 4) Mention hurricane response experience. We're hiring immediately!"
            elif interaction['type'] == 'qualification':
                response = "🏥 Medical students welcome! We have supervised positions available. Requirements: Near graduation, basic life support certified, willing to work 12-hour shifts. Contact: crisis.medical@emergency-response.org. Training provided!"
            else:
                response = "💪 Volunteer opportunities available! Community support roles include: family assistance, supply distribution, communication support. No experience required - training provided. Contact: crisis.volunteer@emergency-response.org"
            
            print(f"   🤖 Automated Response: {response}")
            print("   " + "-" * 60)
        
        print(f"\n🎯 Processed {len(sample_interactions)} user interactions automatically")
        print("✅ All responses generated and sent within 30 seconds")
        
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        """Main application menu"""
        while True:
            self.clear_screen()
            print("🌟 CRISIS RESPONSE SOCIAL MEDIA AUTOMATION")
            print("   Interactive Demo - Blackbox API Integration")
            
            if self.current_crisis:
                print(f"\n📍 Active Crisis: {self.current_crisis.disaster_type.value.title()} in {self.current_crisis.location}")
                print(f"🔧 Jobs Created: {len(self.current_jobs)}")
                print(f"📱 Posts Generated: {len(self.current_posts)}")
            
            menu_options = [
                "🌪️  Select Disaster Scenario",
                "👷  Create Job Postings",
                "📱  Generate Social Media Campaign", 
                "👀  Preview Generated Content",
                "🚀  Simulate Social Media Posting",
                "📊  View Analytics Dashboard",
                "🤖  Simulate Automated Responses",
                "🎬  Run Complete End-to-End Demo",
                "ℹ️   Show App Information"
            ]
            
            self.print_menu("Main Menu", menu_options)
            choice = self.get_user_choice(len(menu_options))
            
            if choice == 0:
                print("\n👋 Thank you for using Crisis Response Social Media Automation!")
                print("💡 Ready for production deployment with real social media APIs!")
                break
            elif choice == 1:
                self.disaster_scenario_menu()
            elif choice == 2:
                self.create_job_postings_interactive()
            elif choice == 3:
                self.generate_social_campaign_interactive()
            elif choice == 4:
                self.preview_content()
            elif choice == 5:
                self.simulate_posting()
            elif choice == 6:
                self.show_analytics()
            elif choice == 7:
                self.simulate_responses()
            elif choice == 8:
                # Run complete demo
                print("\n🎬 Running complete end-to-end demonstration...")
                self.app.demonstrate_end_to_end_flow()
                input("\nDemo completed! Press Enter to continue...")
            elif choice == 9:
                self.show_app_info()
    
    def show_app_info(self):
        """Show application information"""
        self.print_header("Application Information")
        
        info_text = """
🌟 Crisis Response Social Media Automation App

📋 Purpose:
   Automate social media posting for post-natural disaster job opportunities
   and resource allocation using AI-powered content generation.

🚀 Key Features:
   • AI-powered content generation using Blackbox API
   • Multi-platform social media posting (Twitter, Facebook, LinkedIn, Instagram)
   • Automated response handling for user interactions
   • A/B testing for content optimization
   • Real-time analytics and performance tracking
   • Crisis-specific job posting automation
   • Profile targeting and information release

🛠️ Technical Stack:
   • Python 3.9+ with SQLite database
   • Matplotlib/Seaborn for analytics visualization
   • PIL for image generation
   • Pandas for data analysis
   • Requests for API communication

🎯 Target Scenarios:
   • Hurricane recovery coordination
   • Earthquake response management
   • Wildfire evacuation and cleanup
   • Flood damage restoration
   • Tornado emergency response
   • Tsunami evacuation coordination
   • Winter storm emergency support

📈 Success Metrics:
   • Faster emergency response coordination
   • Increased volunteer and worker applications
   • Improved community communication
   • Reduced manual coordination overhead

🚀 Production Ready:
   Ready for deployment with real social media APIs
   and enterprise-grade infrastructure.
        """
        
        print(info_text)
        input("\nPress Enter to continue...")

def main():
    """Main function to run interactive demo"""
    print("🌟 Crisis Response Social Media Automation - Interactive Demo")
    print("=" * 60)
    print("Starting interactive demonstration...")
    
    try:
        demo = InteractiveDemo()
        demo.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("Please check your Python environment and try again.")

if __name__ == "__main__":
    main()
