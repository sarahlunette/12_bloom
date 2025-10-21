#!/usr/bin/env python3
"""
REST API Server for Crisis Response Social Media Automation
==========================================================

A Flask-based REST API server that provides programmatic access to the
Crisis Response Social Media Automation application.

Endpoints:
- POST /api/crisis - Create a new crisis event
- GET /api/crisis/{id} - Get crisis details
- POST /api/jobs - Create job posting
- GET /api/jobs - List job postings
- POST /api/campaigns - Generate social media campaign
- GET /api/posts - List social media posts
- POST /api/posts/{id}/publish - Publish specific post
- GET /api/analytics - Get analytics data
- POST /api/responses/simulate - Simulate user responses
- GET /api/health - Health check endpoint

Author: Blackbox AI Assistant
"""

import json
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from crisis_response_app import (
    CrisisResponseApp, DisasterType, PlatformType,
    CrisisEvent, JobPosting, SocialMediaPost
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize main application
crisis_app = CrisisResponseApp()

# Global state (in production, use Redis or database)
active_crises = {}
active_jobs = {}
active_posts = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "Crisis Response Social Media API"
    })

@app.route('/api/crisis', methods=['POST'])
def create_crisis():
    """Create a new crisis event"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['disaster_type', 'location', 'severity', 'affected_population']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate disaster type
        try:
            disaster_type = DisasterType(data['disaster_type'])
        except ValueError:
            valid_types = [dt.value for dt in DisasterType]
            return jsonify({
                "error": f"Invalid disaster_type. Valid options: {valid_types}"
            }), 400
        
        # Create crisis event
        crisis = crisis_app.create_crisis_event(
            disaster_type=disaster_type,
            location=data['location'],
            severity=data['severity'],
            affected_population=data['affected_population'],
            job_types=data.get('job_types', []),
            urgent_needs=data.get('urgent_needs', [])
        )
        
        # Store in global state
        active_crises[crisis.id] = crisis
        
        return jsonify({
            "success": True,
            "crisis": {
                "id": crisis.id,
                "disaster_type": crisis.disaster_type.value,
                "location": crisis.location,
                "severity": crisis.severity,
                "affected_population": crisis.affected_population,
                "job_types_needed": crisis.job_types_needed,
                "urgent_needs": crisis.urgent_needs,
                "start_date": crisis.start_date.isoformat(),
                "status": crisis.status
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating crisis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/crisis/<crisis_id>', methods=['GET'])
def get_crisis(crisis_id):
    """Get crisis details by ID"""
    if crisis_id not in active_crises:
        return jsonify({"error": "Crisis not found"}), 404
    
    crisis = active_crises[crisis_id]
    return jsonify({
        "id": crisis.id,
        "disaster_type": crisis.disaster_type.value,
        "location": crisis.location,
        "severity": crisis.severity,
        "affected_population": crisis.affected_population,
        "job_types_needed": crisis.job_types_needed,
        "urgent_needs": crisis.urgent_needs,
        "start_date": crisis.start_date.isoformat(),
        "estimated_duration": crisis.estimated_duration,
        "status": crisis.status
    })

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job posting"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['crisis_id', 'job_title', 'job_type', 'urgency', 'compensation', 'duration']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate crisis exists
        crisis_id = data['crisis_id']
        if crisis_id not in active_crises:
            return jsonify({"error": "Crisis not found"}), 404
        
        crisis = active_crises[crisis_id]
        
        # Create job posting
        job = crisis_app.create_job_posting(
            crisis=crisis,
            job_title=data['job_title'],
            job_type=data['job_type'],
            urgency=data['urgency'],
            requirements=data.get('requirements', []),
            compensation=data['compensation'],
            duration=data['duration'],
            contact_info=data.get('contact_info', f"crisis.{data['job_type']}@emergency-response.org")
        )
        
        # Store in global state
        active_jobs[job.id] = job
        
        return jsonify({
            "success": True,
            "job": {
                "id": job.id,
                "crisis_id": job.crisis_id,
                "job_title": job.job_title,
                "job_type": job.job_type,
                "location": job.location,
                "urgency": job.urgency,
                "requirements": job.requirements,
                "compensation": job.compensation,
                "duration": job.duration,
                "contact_info": job.contact_info,
                "created_at": job.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all job postings"""
    crisis_id = request.args.get('crisis_id')
    
    jobs_list = []
    for job in active_jobs.values():
        if not crisis_id or job.crisis_id == crisis_id:
            jobs_list.append({
                "id": job.id,
                "crisis_id": job.crisis_id,
                "job_title": job.job_title,
                "job_type": job.job_type,
                "location": job.location,
                "urgency": job.urgency,
                "requirements": job.requirements,
                "compensation": job.compensation,
                "duration": job.duration,
                "contact_info": job.contact_info,
                "created_at": job.created_at.isoformat()
            })
    
    return jsonify({
        "success": True,
        "jobs": jobs_list,
        "count": len(jobs_list)
    })

@app.route('/api/campaigns', methods=['POST'])
def generate_campaign():
    """Generate social media campaign"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['crisis_id', 'job_id', 'platforms']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate crisis and job exist
        crisis_id = data['crisis_id']
        job_id = data['job_id']
        
        if crisis_id not in active_crises:
            return jsonify({"error": "Crisis not found"}), 404
        if job_id not in active_jobs:
            return jsonify({"error": "Job not found"}), 404
        
        crisis = active_crises[crisis_id]
        job = active_jobs[job_id]
        
        # Validate platforms
        platforms = []
        for platform_str in data['platforms']:
            try:
                platform = PlatformType(platform_str)
                platforms.append(platform)
            except ValueError:
                valid_platforms = [pt.value for pt in PlatformType]
                return jsonify({
                    "error": f"Invalid platform: {platform_str}. Valid options: {valid_platforms}"
                }), 400
        
        # Generate schedule times
        schedule_offset = data.get('schedule_offset_minutes', 5)
        schedule_times = [
            datetime.now() + timedelta(minutes=schedule_offset),
            datetime.now() + timedelta(hours=1),
            datetime.now() + timedelta(hours=3),
            datetime.now() + timedelta(hours=6)
        ]
        
        # Generate campaign
        posts = crisis_app.generate_social_media_campaign(
            crisis=crisis,
            job=job,
            platforms=platforms,
            schedule_times=schedule_times
        )
        
        # Store posts in global state
        for post in posts:
            active_posts[post.id] = post
        
        # Prepare response
        posts_data = []
        for post in posts:
            posts_data.append({
                "id": post.id,
                "platform": post.platform.value,
                "content": post.content,
                "media_path": post.media_path,
                "scheduled_time": post.scheduled_time.isoformat(),
                "crisis_id": post.crisis_id,
                "job_id": post.job_id,
                "hashtags": post.hashtags,
                "status": post.status,
                "ab_test_group": post.ab_test_group
            })
        
        return jsonify({
            "success": True,
            "campaign": {
                "crisis_id": crisis_id,
                "job_id": job_id,
                "platforms": [p.value for p in platforms],
                "posts": posts_data,
                "total_posts": len(posts_data)
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error generating campaign: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts', methods=['GET'])
def list_posts():
    """List social media posts"""
    crisis_id = request.args.get('crisis_id')
    job_id = request.args.get('job_id')
    platform = request.args.get('platform')
    status = request.args.get('status')
    
    posts_list = []
    for post in active_posts.values():
        # Apply filters
        if crisis_id and post.crisis_id != crisis_id:
            continue
        if job_id and post.job_id != job_id:
            continue
        if platform and post.platform.value != platform:
            continue
        if status and post.status != status:
            continue
        
        posts_list.append({
            "id": post.id,
            "platform": post.platform.value,
            "content": post.content,
            "media_path": post.media_path,
            "scheduled_time": post.scheduled_time.isoformat(),
            "crisis_id": post.crisis_id,
            "job_id": post.job_id,
            "hashtags": post.hashtags,
            "status": post.status,
            "engagement_metrics": post.engagement_metrics,
            "ab_test_group": post.ab_test_group
        })
    
    return jsonify({
        "success": True,
        "posts": posts_list,
        "count": len(posts_list)
    })

@app.route('/api/posts/<post_id>/publish', methods=['POST'])
def publish_post(post_id):
    """Publish a specific post"""
    if post_id not in active_posts:
        return jsonify({"error": "Post not found"}), 404
    
    post = active_posts[post_id]
    
    # Simulate posting
    success = crisis_app.social_media_manager.post_to_platform(post)
    
    if success:
        active_posts[post_id] = post  # Update stored post
        return jsonify({
            "success": True,
            "post": {
                "id": post.id,
                "platform": post.platform.value,
                "status": post.status,
                "engagement_metrics": post.engagement_metrics,
                "published_at": datetime.now().isoformat()
            }
        })
    else:
        return jsonify({
            "success": False,
            "error": "Failed to publish post"
        }), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data"""
    try:
        analytics = crisis_app.analytics_manager.generate_analytics_report()
        
        # Generate visualization if requested
        include_viz = request.args.get('include_visualization', 'false').lower() == 'true'
        if include_viz:
            viz_path = crisis_app.analytics_manager.create_analytics_visualization()
            analytics['visualization_path'] = viz_path
        
        return jsonify({
            "success": True,
            "analytics": analytics,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating analytics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/responses/simulate', methods=['POST'])
def simulate_responses():
    """Simulate user responses and automated replies"""
    try:
        data = request.get_json()
        response_count = data.get('count', 5)
        
        # Simulate processing
        crisis_app.response_handler.process_responses()
        
        # Generate sample responses
        sample_responses = [
            {
                "id": f"resp_{i}",
                "user": f"@user_{i}",
                "platform": "twitter",
                "message": f"Sample user response {i}",
                "type": ["availability", "application", "information"][i % 3],
                "automated_reply": "Thank you for your interest! We'll get back to you soon.",
                "timestamp": datetime.now().isoformat()
            }
            for i in range(response_count)
        ]
        
        return jsonify({
            "success": True,
            "responses": sample_responses,
            "processed_count": response_count
        })
        
    except Exception as e:
        logger.error(f"Error simulating responses: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/visualization/<path:filename>')
def serve_visualization(filename):
    """Serve generated visualization files"""
    try:
        return send_file(f"/vercel/sandbox/{filename}", mimetype='image/png')
    except Exception as e:
        return jsonify({"error": "File not found"}), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "POST /api/crisis - Create crisis event",
            "GET /api/crisis/{id} - Get crisis details",
            "POST /api/jobs - Create job posting",
            "GET /api/jobs - List jobs",
            "POST /api/campaigns - Generate campaign",
            "GET /api/posts - List posts",
            "POST /api/posts/{id}/publish - Publish post",
            "GET /api/analytics - Get analytics",
            "POST /api/responses/simulate - Simulate responses",
            "GET /api/health - Health check"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "Please try again or contact support"
    }), 500

def main():
    """Main function to run the API server"""
    print("🚀 Starting Crisis Response Social Media API Server")
    print("=" * 60)
    print("Available endpoints:")
    print("• POST /api/crisis - Create crisis event")
    print("• GET /api/crisis/{id} - Get crisis details")  
    print("• POST /api/jobs - Create job posting")
    print("• GET /api/jobs - List jobs")
    print("• POST /api/campaigns - Generate campaign")
    print("• GET /api/posts - List posts")
    print("• POST /api/posts/{id}/publish - Publish post")
    print("• GET /api/analytics - Get analytics")
    print("• POST /api/responses/simulate - Simulate responses")
    print("• GET /api/health - Health check")
    print("=" * 60)
    print("🌐 Server will start on http://localhost:5000")
    print("📚 API documentation available in code comments")
    print("🛡️  CORS enabled for frontend integration")
    
    # Note: In production, don't run with debug=True
    # app.run(host='0.0.0.0', port=5000, debug=False)
    print("\n⚠️  WARNING: Server start disabled in sandbox environment")
    print("In production, uncomment the app.run() line to start the server")

if __name__ == "__main__":
    main()
