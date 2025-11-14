import os
import xml.etree.ElementTree as ET
import requests
import sys

try:
    tree = ET.parse('report.xml')
    root = tree.getroot()

    tests = int(root.attrib.get('tests', 0))
    failures = int(root.attrib.get('failures', 0))
    errors = int(root.attrib.get('errors', 0))
    skipped = int(root.attrib.get('skipped', 0)) if 'skipped' in root.attrib else 0
    passed = tests - failures - errors - skipped

    state = 'SUCCESS' if failures == 0 and errors == 0 else 'FAILURE'
    summary = f'Tests: {tests}, Passed: {passed}, Failures: {failures}, Errors: {errors}, Skipped: {skipped}'

    payload = {'text': f':robot_face: *CI Test Report - {state}*\n{summary}'}

    webhook = os.getenv('SLACK_WEBHOOK')
    if webhook:
        response = requests.post(webhook, json=payload, timeout=10)
        response.raise_for_status()
        print(f'Slack notification sent successfully: {state}')
    else:
        print('SLACK_WEBHOOK is not set')

except FileNotFoundError:
    print('Error: report.xml not found')
    sys.exit(1)
except Exception as e:
    print(f'Error sending Slack message: {e}')
    sys.exit(1)