from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import requests
import json
from datetime import datetime, timedelta
from .models import Todo

def home(request):
    try:
        return render(request, 'core/home.html')
    except Exception as e:
        # Fallback response if template rendering fails
        return JsonResponse({'status': 'ok', 'message': 'Django app is running'})

def health_check(request):
    """Simple health check endpoint for Railway"""
    return JsonResponse({'status': 'healthy', 'message': 'Django app is running'})

def debug_info(request):
    """Debug endpoint to help troubleshoot Railway deployment"""
    import os
    import sys
    from django.conf import settings
    
    debug_info = {
        'status': 'ok',
        'django_version': settings.VERSION,
        'python_version': sys.version,
        'port': os.environ.get('PORT', 'not set'),
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'static_url': settings.STATIC_URL,
        'static_root': getattr(settings, 'STATIC_ROOT', 'not set'),
    }
    return JsonResponse(debug_info)

def leetcode_daily(request):
    try:
        # LeetCode GraphQL endpoint
        url = "https://leetcode.com/graphql/"
        
        # GraphQL query to get the daily question
        query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                userStatus
                link
                question {
                    acRate
                    difficulty
                    freqBar
                    frontendQuestionId: questionFrontendId
                    isFavor
                    paidOnly: isPaidOnly
                    status
                    title
                    titleSlug
                    hasVideoSolution
                    hasSolution
                    topicTags {
                        name
                        id
                        slug
                    }
                    content
                    exampleTestcases
                    hints
                    metaData
                }
            }
        }
        """
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.post(url, json={'query': query}, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            daily_question = data.get('data', {}).get('activeDailyCodingChallengeQuestion', {})
            
            if daily_question:
                context = {
                    'question': daily_question.get('question', {}),
                    'date': daily_question.get('date', ''),
                    'link': daily_question.get('link', ''),
                    'user_status': daily_question.get('userStatus', ''),
                    'error': None
                }
            else:
                context = {'error': 'No daily question found'}
        else:
            context = {'error': f'Failed to fetch data: {response.status_code}'}
            
    except requests.RequestException as e:
        context = {'error': f'Network error: {str(e)}'}
    except Exception as e:
        context = {'error': f'Unexpected error: {str(e)}'}
    
    return render(request, 'core/leetcode_daily.html', context)

def leetcode_recent(request):
    try:
        # LeetCode GraphQL endpoint
        url = "https://leetcode.com/graphql/"
        
        # Get current year and month
        from datetime import datetime
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        
        # GraphQL query to get recent daily questions with required year and month parameters
        query = """
        query recentDailyQuestions($year: Int!, $month: Int!) {
            dailyCodingChallengeV2(year: $year, month: $month) {
                challenges {
                    date
                    userStatus
                    link
                    question {
                        acRate
                        difficulty
                        freqBar
                        frontendQuestionId: questionFrontendId
                        isFavor
                        paidOnly: isPaidOnly
                        status
                        title
                        titleSlug
                        hasVideoSolution
                        hasSolution
                        topicTags {
                            name
                            id
                            slug
                        }
                        content
                        exampleTestcases
                        hints
                        metaData
                    }
                }
            }
        }
        """
        
        variables = {
            "year": current_year,
            "month": current_month
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Debug: Print the response structure
            print("API Response:", data)
            
            # Check if we have data and errors
            if 'errors' in data:
                context = {'error': f'API Error: {data["errors"]}'}
            elif 'data' in data and data['data']:
                # Try to get challenges from the response
                challenges = None
                if 'dailyCodingChallengeV2' in data['data'] and data['data']['dailyCodingChallengeV2']:
                    challenges = data['data']['dailyCodingChallengeV2'].get('challenges', [])
                
                if challenges and len(challenges) > 0:
                    # Get the last 5 questions (most recent first)
                    recent_questions = challenges[:5]
                    
                    context = {
                        'questions': recent_questions,
                        'error': None
                    }
                else:
                    # Fallback: Create mock data for demonstration
                    context = {
                        'questions': [
                            {
                                'date': '2025-09-05',
                                'link': '/problems/sample-problem-1',
                                'question': {
                                    'title': 'Sample Problem 1',
                                    'difficulty': 'Easy',
                                    'acRate': 75.5,
                                    'frontendQuestionId': '1',
                                    'paidOnly': False,
                                    'topicTags': [{'name': 'Array'}, {'name': 'Hash Table'}]
                                }
                            },
                            {
                                'date': '2025-09-04',
                                'link': '/problems/sample-problem-2',
                                'question': {
                                    'title': 'Sample Problem 2',
                                    'difficulty': 'Medium',
                                    'acRate': 45.2,
                                    'frontendQuestionId': '2',
                                    'paidOnly': False,
                                    'topicTags': [{'name': 'Dynamic Programming'}, {'name': 'String'}]
                                }
                            },
                            {
                                'date': '2025-09-03',
                                'link': '/problems/sample-problem-3',
                                'question': {
                                    'title': 'Sample Problem 3',
                                    'difficulty': 'Hard',
                                    'acRate': 25.8,
                                    'frontendQuestionId': '3',
                                    'paidOnly': True,
                                    'topicTags': [{'name': 'Graph'}, {'name': 'BFS'}]
                                }
                            },
                            {
                                'date': '2025-09-02',
                                'link': '/problems/sample-problem-4',
                                'question': {
                                    'title': 'Sample Problem 4',
                                    'difficulty': 'Easy',
                                    'acRate': 82.1,
                                    'frontendQuestionId': '4',
                                    'paidOnly': False,
                                    'topicTags': [{'name': 'Math'}, {'name': 'Simulation'}]
                                }
                            },
                            {
                                'date': '2025-09-01',
                                'link': '/problems/sample-problem-5',
                                'question': {
                                    'title': 'Sample Problem 5',
                                    'difficulty': 'Medium',
                                    'acRate': 38.7,
                                    'frontendQuestionId': '5',
                                    'paidOnly': False,
                                    'topicTags': [{'name': 'Tree'}, {'name': 'DFS'}]
                                }
                            }
                        ],
                        'error': 'Using sample data - API endpoint may have changed'
                    }
            else:
                context = {'error': 'No data received from API'}
        else:
            context = {'error': f'Failed to fetch data: {response.status_code}'}
            
    except requests.RequestException as e:
        context = {'error': f'Network error: {str(e)}'}
    except Exception as e:
        context = {'error': f'Unexpected error: {str(e)}'}
    
    return render(request, 'core/leetcode_recent.html', context)

def leetcode_question_detail(request, question_slug):
    try:
        # LeetCode GraphQL endpoint
        url = "https://leetcode.com/graphql/"
        
        # GraphQL query to get specific question details
        query = """
        query questionContent($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                content
                difficulty
                likes
                dislikes
                isLiked
                similarQuestions
                contributors {
                    username
                    profileUrl
                    avatarUrl
                    __typename
                }
                topicTags {
                    name
                    slug
                    translatedName
                    __typename
                }
                companyTagStats
                codeSnippets {
                    lang
                    langSlug
                    code
                    __typename
                }
                stats
                hints
                solution {
                    id
                    canSeeDetail
                    paidOnly
                    hasVideoSolution
                    paidOnlyVideo
                    __typename
                }
                status
                sampleTestCase
                metaData
                judgerAvailable
                judgeType
                mysqlSchemas
                enableRunCode
                enableTestMode
                enableDebugger
                envInfo
                libraryUrl
                questionDetailUrl
                __typename
            }
        }
        """
        
        variables = {
            "titleSlug": question_slug
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'errors' in data:
                context = {'error': f'API Error: {data["errors"]}'}
            elif 'data' in data and data['data'] and data['data']['question']:
                question = data['data']['question']
                
                # Parse stats if available
                stats = {}
                if question.get('stats'):
                    import json
                    try:
                        stats = json.loads(question['stats'])
                    except:
                        stats = {}
                
                context = {
                    'question': question,
                    'stats': stats,
                    'error': None
                }
            else:
                context = {'error': 'Question not found'}
        else:
            context = {'error': f'Failed to fetch data: {response.status_code}'}
            
    except requests.RequestException as e:
        context = {'error': f'Network error: {str(e)}'}
    except Exception as e:
        context = {'error': f'Unexpected error: {str(e)}'}
    
    return render(request, 'core/leetcode_question_detail.html', context)

def todo_list(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'core/todo_list.html', context)

def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        status = request.POST.get('status', 'pending')
        due_date_str = request.POST.get('due_date', '')
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass
        
        todo = Todo.objects.create(
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date
        )
        messages.success(request, f'ToDo "{todo.title}" created successfully!')
        return redirect('todo_list')
    
    return render(request, 'core/todo_form.html', {'form_type': 'create'})

def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description', '')
        todo.priority = request.POST.get('priority', 'medium')
        todo.status = request.POST.get('status', 'pending')
        due_date_str = request.POST.get('due_date', '')
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass
        todo.due_date = due_date
        
        todo.save()
        messages.success(request, f'ToDo "{todo.title}" updated successfully!')
        return redirect('todo_list')
    
    context = {
        'todo': todo,
        'form_type': 'update'
    }
    return render(request, 'core/todo_form.html', context)

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo_title = todo.title
        todo.delete()
        messages.success(request, f'ToDo "{todo_title}" deleted successfully!')
        return redirect('todo_list')
    
    context = {
        'todo': todo,
    }
    return render(request, 'core/todo_confirm_delete.html', context)
