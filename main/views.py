from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
import json
import requests
import uuid
import io
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import urlparse
from .storage import CloudflareR2Storage
import random

# 创建R2存储实例
r2_storage = CloudflareR2Storage()

from django.utils.crypto import get_random_string
from .models import PersonalInformation
import os
import math
from PIL import ImageFilter
from django.utils.html import strip_tags

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def builder(request):
    if request.method == 'POST':
        # Generate a random unique identifier
        unique_identifier = get_random_string(length=10)

        # Create PersonalInformation object with all details
        personal_info = PersonalInformation.objects.create(
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address', ''),
            dob=request.POST.get('dob', None),
            nationality=request.POST.get('nationality', ''),
            linkedin=request.POST.get('linkedin', ''),
            portfolio=request.POST.get('portfolio', ''),
            unique_identifier=unique_identifier,


            # Education
            degree=request.POST.get('degree', ''),
            field_of_study=request.POST.get('field_of_study', ''),
            institution=request.POST.get('institution', ''),
            institution_location=request.POST.get('institution_location', ''),
            graduation_year=request.POST.get('graduation_year', None),
            gpa=request.POST.get('gpa', None),

            degree_1=request.POST.get('degree_1', ''),
            field_of_study_1=request.POST.get('field_of_study_1', ''),
            institution_1=request.POST.get('institution_1', ''),
            institution_location_1=request.POST.get('institution_location_1', ''),
            graduation_year_1=request.POST.get('graduation_year_1', None) or None,
            gpa_1=request.POST.get('gpa_1', None) or None,


            # Work Experience
            job_title=request.POST.get('job_title', ''),
            company=request.POST.get('company', ''),
            work_location=request.POST.get('work_location', ''),
            employment_dates=request.POST.get('employment_dates', ''),
            responsibilities=request.POST.get('responsibilities', ''),

            job_title_1=request.POST.get('job_title_1', ''),
            company_1=request.POST.get('company_1', ''),
            work_location_1=request.POST.get('work_location_1', ''),
            employment_dates_1=request.POST.get('employment_dates_1', ''),
            responsibilities_1=request.POST.get('responsibilities_1', ''),

            job_title_2=request.POST.get('job_title_2', ''),
            company_2=request.POST.get('company_2', ''),
            work_location_2=request.POST.get('work_location_2', ''),
            employment_dates_2=request.POST.get('employment_dates_2', ''),
            responsibilities_2=request.POST.get('responsibilities_2', ''),
            # achievements=request.POST.get('achievements', ''),


            # Certification
            certification_name=request.POST.get('certification_name', ''),
            issuing_organization=request.POST.get('issuing_organization', ''),
            date_earned=request.POST.get('date_earned', None) or None,

            certification_name_1=request.POST.get('certification_name_1', ''),
            issuing_organization_1=request.POST.get('issuing_organization_1', ''),
            date_earned_1=request.POST.get('date_earned_1', None) or None,


            # Project
            project_title=request.POST.get('project_title', ''),
            project_description=request.POST.get('project_description', ''),
            technologies_used=request.POST.get('technologies_used', ''),
            project_url=request.POST.get('project_url', ''),

            project_title_1=request.POST.get('project_title_1', ''),
            project_description_1=request.POST.get('project_description_1', ''),
            technologies_used_1=request.POST.get('technologies_used_1', ''),
            project_url_1=request.POST.get('project_url_1', ''),

            project_title_2=request.POST.get('project_title_2', ''),
            project_description_2=request.POST.get('project_description_2', ''),
            technologies_used_2=request.POST.get('technologies_used_2', ''),
            project_url_2=request.POST.get('project_url_2', ''),
            # Skills
            technical_skills=request.POST.get('technical_skills', ''),
            soft_skills=request.POST.get('soft_skills', ''),
            # language_proficiency=request.POST.get('language_proficiency', ''),
        )

        # Redirect to the resume page with the unique identifier
        return redirect('resume', unique_identifier=unique_identifier)

    return render(request, 'builder.html', {})


def resume(request, unique_identifier):
    personal_info = get_object_or_404(PersonalInformation, unique_identifier=unique_identifier)
    responsibilities_list = personal_info.responsibilities.split('\n')
    responsibilities_list_1 = personal_info.responsibilities_1.split('\n')
    responsibilities_list_2 = personal_info.responsibilities_2.split('\n')
    technical_skills_list = personal_info.technical_skills.split('\n')
    soft_skills_list = personal_info.soft_skills.split('\n')
    return render(request, 'resume.html', {'personal_info': personal_info, 'responsibilities_list': responsibilities_list, 'technical_skills_list': technical_skills_list, 'soft_skills_list': soft_skills_list, 'responsibilities_list_1': responsibilities_list_1, 'responsibilities_list_2': responsibilities_list_2,})

@csrf_exempt
def generate_festive_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        # 获取当前年份
        current_year = datetime.now().year
        
        # 获取请求参数
        base_prompt = request.POST.get('prompt', '')
        greeting = request.POST.get('greeting', '')
        quality = request.POST.get('quality', 'standard')
        size = request.POST.get('size', '1024x1024')
        style = request.POST.get('style', 'realistic')
        logo = request.FILES.get('logo')
        
        # 初始化R2存储
        r2_storage = default_storage
        
        # 处理Logo
        logo_path = None
        if logo:
            # 使用R2存储Logo
            logo_path = r2_storage.save(f'logos/{uuid.uuid4()}.png', ContentFile(logo.read()))
        
        # 获取 Monica API key
        api_key = os.getenv('MONICA_API_KEY')
        if not api_key:
            return JsonResponse({'error': 'API key not configured'}, status=500)
        
        # 优化提示词，使其更适合中国新年主题
        enhanced_prompt = (
            f"Create a traditional Chinese New Year festive image for {current_year}年 with the following elements: {base_prompt}. "
            "Style: Traditional Chinese painting, vibrant red and gold colors. "
            "Include traditional Chinese New Year elements like lanterns, spring couplets, and auspicious symbols. "
            "Make it festive and culturally authentic. "
        )
        
        # 调用 Monica API 生成图片
        url = "https://openapi.monica.im/v1/image/gen/flux"
        
        payload = {
            "model": "flux_dev",
            "prompt": enhanced_prompt,
            "num_outputs": 1,
            "size": size,  # 直接使用原始的 size 字符串，如 "1024x1024"
            "seed": random.randint(1, 1000),  # 随机种子以获得不同的生成结果
            "steps": 25,
            "guidance": "3",
            "interval": 2,
            "safety_tolerance": 2
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"Sending request to Monica API with payload: {payload}")
        response = requests.request("POST", url, json=payload, headers=headers)
        print(f"Monica API response status: {response.status_code}")
        print(f"Monica API response: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"Monica API response: {result}")
                if 'data' in result and result['data'] and 'url' in result['data'][0]:
                    image_url = result['data'][0]['url']
                    print(f"Generated image URL: {image_url}")
                    return JsonResponse({
                        'success': True,
                        'image_url': image_url
                    })
            except Exception as e:
                print(f"Error parsing Monica API response: {str(e)}")
        
        # 如果API调用失败或解析失败，使用默认模板
        print("Falling back to template generation")
        width, height = map(int, size.split('x'))
        image = Image.new('RGB', (width, height), (198, 40, 40))  # 使用中国红背景
        
        # 添加装饰性边框
        draw = ImageDraw.Draw(image)
        border_width = 20
        draw.rectangle(
            [(border_width, border_width), 
             (width - border_width, height - border_width)], 
            outline=(255, 215, 0),  # 金色边框
            width=3
        )
        
        # 使用默认字体添加新年祝福
        font = None
        font_errors = []
        
        # 尝试加载字体的顺序
        font_paths = [
            os.path.join(settings.STATIC_ROOT, 'fonts', 'SimHei.ttf'),
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/Arial Unicode.ttf'
        ]
        
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, min(image.width, image.height) // 15)
                    print(f"Successfully loaded font from: {font_path}")
                    break
                else:
                    font_errors.append(f"Font file not found: {font_path}")
            except Exception as e:
                font_errors.append(f"Error loading font {font_path}: {str(e)}")
        
        if font is None:
            print("All font loading attempts failed:")
            for error in font_errors:
                print(f"  - {error}")
            print("Falling back to default font")
            font = ImageFont.load_default()
            font_size = 24  # 默认字体需要较小的尺寸
        
        text = f"{current_year}年新年快乐"
        
        # 增加文字大小
        large_font_size = height // 10
        # 创建一个临时图像来绘制放大的文字
        temp_img = Image.new('RGB', (width * 2, height * 2), (198, 40, 40))
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((width // 2, height // 2), text, 
                      font=font, fill=(255, 215, 0),  # 金色文字
                      anchor="mm")  # 居中对齐
        # 将临时图像缩小回原始大小，这样文字会显得更清晰
        temp_img = temp_img.resize((width, height), Image.Resampling.LANCZOS)
        image.paste(temp_img, (0, 0))
        
        # 添加装饰性图案
        for i in range(4):  # 在四个角落添加简单的装饰
            x = border_width * 2 if i % 2 == 0 else width - border_width * 2
            y = border_width * 2 if i < 2 else height - border_width * 2
            draw.ellipse(
                [(x - 10, y - 10), (x + 10, y + 10)],
                fill=(255, 215, 0)  # 金色装饰
            )
        
        # 如果有Logo，添加到图片上
        if logo_path:
            try:
                # 从R2获取Logo
                logo_content = r2_storage.open(logo_path).read()
                logo = Image.open(io.BytesIO(logo_content))
                
                # 调整Logo大小
                logo_size = min(image.width, image.height) // 4
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # 计算Logo位置（右下角）
                position = (image.width - logo_size - 20, image.height - logo_size - 20)
                
                # 确保Logo有透明通道
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')
                
                # 将Logo粘贴到图片上
                image.paste(logo, position, logo)
                
            except Exception as e:
                print(f"Error adding logo: {str(e)}")
        
        # 如果有祝福语，添加到图片上
        if greeting:
            try:
                # 创建一个支持透明度的图层
                txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(txt_layer)
                
                # 计算合适的字体大小（根据图片尺寸）
                font_size = min(image.width, image.height) // 15
                
                # 尝试加载字体
                font = None
                font_errors = []
                
                # 尝试加载字体的顺序
                font_paths = [
                    os.path.join(settings.STATIC_ROOT, 'fonts', 'SimHei.ttf'),
                    '/System/Library/Fonts/PingFang.ttc',
                    '/System/Library/Fonts/STHeiti Light.ttc',
                    '/System/Library/Fonts/Arial Unicode.ttf'
                ]
                
                for font_path in font_paths:
                    try:
                        if os.path.exists(font_path):
                            font = ImageFont.truetype(font_path, font_size)
                            print(f"Successfully loaded font from: {font_path}")
                            break
                        else:
                            font_errors.append(f"Font file not found: {font_path}")
                    except Exception as e:
                        font_errors.append(f"Error loading font {font_path}: {str(e)}")
                
                if font is None:
                    print("All font loading attempts failed:")
                    for error in font_errors:
                        print(f"  - {error}")
                    print("Falling back to default font")
                    font = ImageFont.load_default()
                    font_size = 24  # 默认字体需要较小的尺寸
                
                # 计算文本大小
                text_bbox = draw.textbbox((0, 0), greeting, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # 计算文本位置（水平居中，垂直位置在顶部）
                x = (image.width - text_width) // 2
                y = 50  # 距离顶部50像素
                
                # 添加发光效果（黑色光晕）
                glow_range = 3
                glow_opacity = 80  # 增加发光效果的不透明度
                for i in range(glow_range, -1, -1):
                    opacity = int(glow_opacity * (1 - i/glow_range))
                    for angle in range(0, 360, 30):  # 12个方向的发光，使发光更均匀
                        dx = int(i * math.cos(math.radians(angle)))
                        dy = int(i * math.sin(math.radians(angle)))
                        draw.text(
                            (x + dx, y + dy),
                            greeting,
                            font=font,
                            fill=(0, 0, 0, opacity)  # 黑色光晕
                        )
                
                # 添加主文本（纯白色）
                draw.text((x, y), greeting, font=font, fill=(255, 255, 255, 255))
                
                # 应用轻微的高斯模糊，使文字更柔和
                txt_layer = txt_layer.filter(ImageFilter.GaussianBlur(radius=0.3))
                
                # 将文本图层合并到原图
                image = Image.alpha_composite(image.convert('RGBA'), txt_layer)
                
                print(f"Successfully added greeting text: {greeting}")
            except Exception as e:
                print(f"Error adding greeting: {str(e)}")
                print(f"Greeting text was: {greeting}")
        
        # 保存处理后的图片到R2
        output = io.BytesIO()
        image.save(output, format='PNG', quality=95)
        output.seek(0)
        
        # 生成唯一的文件名并保存到R2
        unique_filename = f"generated/festive_{uuid.uuid4()}.png"
        saved_path = r2_storage.save(unique_filename, ContentFile(output.getvalue()))
        
        # 构建完整的公开访问URL
        image_url = f"{settings.CLOUDFLARE_R2_PUBLIC_URL}/{saved_path}"
        
        print(f"Generated image URL: {image_url}")  # 添加调试信息
        
        return JsonResponse({
            'success': True,
            'image_url': image_url
        })
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
def send_festive_email(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        recipient_email = data.get('recipient_email')
        subject = data.get('subject', '新年贺卡')
        message = data.get('message', '')
        image_url = data.get('image_url')
        
        if not recipient_email or not image_url:
            return JsonResponse({'error': '缺少必要参数'}, status=400)
        
        try:
            # 准备邮件内容
            html_content = render_to_string('email/festive_email.html', {
                'message': message,
                'year': datetime.now().year,
                'image_url': image_url  # 直接使用 R2 的 URL
            })
            
            # 创建邮件对象
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email]
            )
            
            # 设置内容类型为HTML
            email.content_subtype = "html"
            
            # 发送邮件
            email.send(fail_silently=False)
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return JsonResponse({'error': '发送邮件失败'}, status=500)
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return JsonResponse({'error': '处理请求失败'}, status=400)

def festive_maker(request):
    return render(request, 'festive-maker.html')
