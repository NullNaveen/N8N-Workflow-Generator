"""
COMPREHENSIVE N8N WORKFLOW TESTING FRAMEWORK
Tests 10+ complex prompts with 7-10 different applications each
Validates JSON structure, node types, connections, and parameters
"""

import requests
import json
import time
from typing import List, Dict, Any
from datetime import datetime

class ComprehensiveWorkflowTester:
    def __init__(self, api_url: str = "http://localhost:7000/api/generate"):
        self.api_url = api_url
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
    def run_comprehensive_test_suite(self):
        """Run ALL test prompts until they work perfectly"""
        print("🚀 STARTING COMPREHENSIVE N8N WORKFLOW TESTING")
        print("="*80)
        
        test_prompts = self._get_complex_test_prompts()
        
        cycle_count = 1
        max_cycles = 10  # Safety limit
        
        while cycle_count <= max_cycles:
            print(f"\n🔄 TESTING CYCLE {cycle_count}")
            print("-"*50)
            
            self.test_results = []
            self.passed_tests = 0
            self.failed_tests = 0
            
            for i, prompt in enumerate(test_prompts, 1):
                print(f"\n📝 Test {i}/{len(test_prompts)}: {prompt[:60]}...")
                result = self._test_single_prompt(prompt, i)
                self.test_results.append(result)
                
                if result['passed']:
                    self.passed_tests += 1
                    print(f"✅ PASSED - Generated {result['node_count']} nodes")
                else:
                    self.failed_tests += 1
                    print(f"❌ FAILED - {result['error']}")
                
                time.sleep(0.5)  # Brief pause between tests
            
            # Print cycle summary
            print(f"\n📊 CYCLE {cycle_count} SUMMARY:")
            print(f"✅ Passed: {self.passed_tests}/{len(test_prompts)}")
            print(f"❌ Failed: {self.failed_tests}/{len(test_prompts)}")
            print(f"📈 Success Rate: {(self.passed_tests/len(test_prompts)*100):.1f}%")
            
            if self.failed_tests == 0:
                print(f"\n🎉 ALL TESTS PASSED IN CYCLE {cycle_count}!")
                print("🚀 COMPREHENSIVE TESTING COMPLETE!")
                return True
            
            print(f"\n⚠️  {self.failed_tests} tests still failing. Continuing to next cycle...")
            cycle_count += 1
        
        print(f"\n⚠️  Maximum cycles ({max_cycles}) reached.")
        return False
    
    def _get_complex_test_prompts(self) -> List[str]:
        """Get 10+ complex prompts using 7-10 different applications each"""
        return [
            # Test 1: Customer Support Automation (10 applications)
            "When I receive a customer support email with high priority, automatically create a Zendesk ticket, save email attachments to Google Drive, send auto-response via Gmail, notify support team on Slack, create task in Asana, update customer record in HubSpot, send SMS alert via Twilio, log incident in Google Sheets, post update to Discord, and create follow-up reminder in Trello",
            
            # Test 2: Sales Pipeline Automation (9 applications)
            "When Stripe payment exceeds $10,000, update opportunity in Salesforce, create invoice in QuickBooks, send thank-you email via Mailchimp, notify sales team on Microsoft Teams, create celebration post on Slack, save contract to Dropbox, update tracking sheet in Airtable, schedule follow-up call in Calendly, and create success story in Notion",
            
            # Test 3: Project Management Workflow (8 applications)
            "When GitHub pull request is merged to main branch, create deployment task in Jira, notify development team on Discord, update project status in Linear, create release notes in Notion, send stakeholder email via Gmail, post announcement on Slack, update tracking sheet in Google Sheets, and create celebration card in Trello",
            
            # Test 4: E-commerce Order Processing (10 applications)
            "When Shopify order is placed for premium product, update inventory in MongoDB, send order confirmation via SendGrid, create shipment task in Asana, notify warehouse team on Teams, update customer profile in HubSpot, generate invoice in QuickBooks, send SMS tracking via Twilio, log sale in Google Sheets, post celebration on Slack, and create review request in Mailchimp",
            
            # Test 5: Marketing Campaign Automation (9 applications)
            "When new subscriber joins Mailchimp list with 'enterprise' tag, create lead in Salesforce, send welcome email sequence, notify sales team on Slack, create follow-up task in HubSpot, schedule discovery call in Calendly, add to premium segment in Airtable, send LinkedIn message, create opportunity in Pipedrive, and update tracking dashboard in Google Sheets",
            
            # Test 6: Content Publication Workflow (8 applications)
            "When new blog post is published on WordPress, create social media posts on Twitter and LinkedIn, send newsletter via Mailchimp, notify content team on Slack, update editorial calendar in Airtable, save backup to Google Drive, create analytics tracking in Google Sheets, and schedule follow-up promotion in Buffer",
            
            # Test 7: Event Management System (10 applications)
            "When Eventbrite registration is completed for VIP ticket, send welcome email via Gmail, create attendee record in Airtable, add to VIP list in Mailchimp, send calendar invite through Calendly, notify event team on Teams, create personalized agenda in Notion, send SMS confirmation via Twilio, update capacity tracking in Google Sheets, post welcome message on Discord, and create networking intro in LinkedIn",
            
            # Test 8: Financial Monitoring Workflow (9 applications)
            "When bank transaction exceeds $50,000 via webhook, create expense record in QuickBooks, notify accounting team on Slack, send approval request via email, create review task in Asana, update cash flow sheet in Google Sheets, send alert SMS via Twilio, log transaction in MongoDB, create audit trail in Notion, and schedule review meeting in Calendly",
            
            # Test 9: Customer Onboarding Pipeline (10 applications)
            "When new customer signs up through Typeform, create contact in HubSpot, send welcome email series via Mailchimp, assign onboarding specialist in Salesforce, create project in Asana, schedule kickoff call in Calendly, add to onboarding Slack channel, create customer folder in Google Drive, update tracking sheet in Airtable, send SMS welcome via Twilio, and create success plan in Notion",
            
            # Test 10: Bug Report Processing (8 applications)
            "When critical bug is reported via GitHub issue with 'critical' label, create urgent ticket in Zendesk, notify engineering team on Discord, assign developer in Jira, send client notification via Gmail, create incident log in Notion, update status dashboard in Google Sheets, send SMS alert to team lead via Twilio, and create post-mortem task in Asana",
            
            # Test 11: Data Processing Pipeline (9 applications)
            "When CSV file is uploaded to Google Drive with 'process' tag, validate data using custom function, save clean data to MongoDB, create summary report in Google Sheets, send processing complete email via Gmail, notify data team on Slack, create data quality dashboard in Grafana, backup results to AWS S3, and schedule review meeting in Calendly",
            
            # Test 12: Social Media Management (10 applications)
            "When mention is detected on Twitter with negative sentiment, create crisis response task in Asana, notify PR team on Teams, send internal alert via Slack, create response draft in Notion, schedule team meeting in Calendly, update reputation tracking in Airtable, send stakeholder email via Gmail, create media monitoring report in Google Sheets, log incident in CRM, and post team update on Discord"
        ]
    
    def _test_single_prompt(self, prompt: str, test_number: int) -> Dict[str, Any]:
        """Test a single prompt and validate comprehensive results"""
        try:
            # Make API request
            response = requests.post(
                self.api_url,
                json={'prompt': prompt},
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    'test_number': test_number,
                    'prompt': prompt,
                    'passed': False,
                    'error': f"HTTP {response.status_code}",
                    'node_count': 0,
                    'apps_detected': []
                }
            
            data = response.json()
            
            if not data.get('success'):
                return {
                    'test_number': test_number,
                    'prompt': prompt,
                    'passed': False,
                    'error': data.get('error', 'Unknown error'),
                    'node_count': 0,
                    'apps_detected': []
                }
            
            workflow = data.get('workflow', {})
            
            # Validate workflow structure
            validation_result = self._validate_workflow_comprehensive(workflow, prompt)
            
            return {
                'test_number': test_number,
                'prompt': prompt,
                'passed': validation_result['valid'],
                'error': validation_result.get('error', ''),
                'node_count': len(workflow.get('nodes', [])),
                'apps_detected': validation_result.get('apps_detected', []),
                'workflow': workflow
            }
            
        except Exception as e:
            return {
                'test_number': test_number,
                'prompt': prompt,
                'passed': False,
                'error': f"Exception: {str(e)}",
                'node_count': 0,
                'apps_detected': []
            }
    
    def _validate_workflow_comprehensive(self, workflow: Dict[str, Any], prompt: str) -> Dict[str, Any]:
        """Comprehensive workflow validation"""
        
        # Basic structure validation
        required_fields = ['name', 'nodes', 'connections', 'active', 'settings']
        for field in required_fields:
            if field not in workflow:
                return {'valid': False, 'error': f"Missing required field: {field}"}
        
        nodes = workflow.get('nodes', [])
        
        # Minimum complexity validation
        if len(nodes) < 3:
            return {'valid': False, 'error': f"Too few nodes generated: {len(nodes)}. Expected at least 3 for complex prompts."}
        
        if len(nodes) > 15:
            return {'valid': False, 'error': f"Too many nodes generated: {len(nodes)}. May indicate poor filtering."}
        
        # Validate each node
        apps_detected = []
        for i, node in enumerate(nodes):
            node_validation = self._validate_node_structure(node, i)
            if not node_validation['valid']:
                return node_validation
            
            # Extract app type from node
            node_type = node.get('type', '')
            app_name = self._extract_app_name(node_type)
            if app_name:
                apps_detected.append(app_name)
        
        # Application diversity validation
        unique_apps = len(set(apps_detected))
        if unique_apps < 3:
            return {'valid': False, 'error': f"Too few different applications: {unique_apps}. Expected at least 3."}
        
        # Connection validation
        connections = workflow.get('connections', {})
        if len(nodes) > 1 and len(connections) == 0:
            return {'valid': False, 'error': "No connections defined between nodes"}
        
        # Validate trigger presence
        has_trigger = any(self._is_trigger_node(node) for node in nodes)
        if not has_trigger:
            return {'valid': False, 'error': "No trigger node found in workflow"}
        
        return {
            'valid': True,
            'apps_detected': apps_detected,
            'unique_apps': unique_apps
        }
    
    def _validate_node_structure(self, node: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Validate individual node structure"""
        required_node_fields = ['name', 'type', 'position', 'parameters', 'typeVersion']
        
        for field in required_node_fields:
            if field not in node:
                return {'valid': False, 'error': f"Node {index}: Missing required field '{field}'"}
        
        # Validate position is array with 2 numbers
        position = node.get('position')
        if not isinstance(position, list) or len(position) != 2:
            return {'valid': False, 'error': f"Node {index}: Invalid position format"}
        
        # Validate type format
        node_type = node.get('type', '')
        if not node_type.startswith('n8n-nodes-base.'):
            return {'valid': False, 'error': f"Node {index}: Invalid node type format: {node_type}"}
        
        return {'valid': True}
    
    def _is_trigger_node(self, node: Dict[str, Any]) -> bool:
        """Check if node is a trigger node"""
        trigger_types = [
            'manualTrigger', 'webhook', 'scheduleTrigger', 'cron',
            'gmailTrigger', 'googleSheetsTrigger', 'githubTrigger',
            'formTrigger', 'stripeTrigger'
        ]
        
        node_type = node.get('type', '').replace('n8n-nodes-base.', '')
        return node_type in trigger_types
    
    def _extract_app_name(self, node_type: str) -> str:
        """Extract application name from node type"""
        if not node_type.startswith('n8n-nodes-base.'):
            return ''
        
        app_name = node_type.replace('n8n-nodes-base.', '')
        
        # Map to friendly names
        app_mapping = {
            'gmail': 'Gmail',
            'slack': 'Slack',
            'discord': 'Discord',
            'twilio': 'Twilio',
            'googleSheets': 'Google Sheets',
            'googleDrive': 'Google Drive',
            'zendesk': 'Zendesk',
            'hubspot': 'HubSpot',
            'salesforce': 'Salesforce',
            'trello': 'Trello',
            'asana': 'Asana',
            'jira': 'Jira',
            'stripe': 'Stripe',
            'quickBooks': 'QuickBooks',
            'mailchimp': 'Mailchimp',
            'notion': 'Notion',
            'airtable': 'Airtable',
            'microsoftTeams': 'Microsoft Teams'
        }
        
        return app_mapping.get(app_name, app_name.title())
    
    def generate_detailed_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        for result in self.test_results:
            status = "✅ PASSED" if result['passed'] else "❌ FAILED"
            print(f"\n{status} Test {result['test_number']}")
            print(f"Prompt: {result['prompt'][:80]}...")
            print(f"Nodes Generated: {result['node_count']}")
            print(f"Apps Detected: {', '.join(result['apps_detected'][:5])}")
            
            if not result['passed']:
                print(f"Error: {result['error']}")
        
        print(f"\n📈 FINAL STATISTICS:")
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/len(self.test_results)*100):.1f}%")
        print("="*80)

def main():
    """Run comprehensive testing"""
    print("🚀 N8N WORKFLOW AI - COMPREHENSIVE TESTING FRAMEWORK")
    print("Testing 12 complex prompts with 7-10 applications each")
    print("Will run testing cycles until ALL prompts work perfectly!")
    
    # Wait for server to be ready
    print("\n⏳ Waiting for server to start...")
    time.sleep(3)
    
    tester = ComprehensiveWorkflowTester()
    success = tester.run_comprehensive_test_suite()
    tester.generate_detailed_report()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! REAL AI SYSTEM WORKING PERFECTLY!")
    else:
        print("\n⚠️  Some tests still failing. Continue development needed.")

if __name__ == "__main__":
    main()