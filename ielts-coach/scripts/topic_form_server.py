#!/usr/bin/env python3
"""
IELTS Coach - Topic Discovery Form Server (v2)

A local server that serves an HTML form for Topic Discovery.
Supports multi-step forms, text input, and image upload.

Usage:
    python topic_form_server.py --config config.json [--port 8765]

Config JSON format:
{
    "steps": [
        {
            "title": "Step 1: Topic Discovery",
            "description": "Please answer the following questions...",
            "questions": [
                {"id": "q1", "label": "What is your favourite food?", "type": "textarea"},
                {"id": "q2", "label": "Do you prefer online shopping?", "type": "radio", "options": ["Online", "In-store", "Both"]}
            ]
        },
        {
            "title": "Step 2: Upload Chart",
            "description": "Please upload your chart image for Task 1",
            "questions": [
                {"id": "chart", "label": "Upload chart image", "type": "image"}
            ]
        }
    ]
}
"""

import http.server
import json
import os
import sys
import webbrowser
import argparse
import threading
import base64
import uuid
from urllib.parse import parse_qs, urlparse

DEFAULT_PORT = 8765

# HTML Form Template with multi-step support
FORM_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS Coach - {title}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .header h1 {{ color: #1a237e; font-size: 1.5rem; margin-bottom: 0.5rem; }}
        .header p {{ color: #666; font-size: 0.9rem; }}
        .topic-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #1a237e, #283593);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 99px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.8rem;
        }}

        /* Step indicators */
        .step-indicators {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}
        .step-dot {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.85rem;
            background: rgba(255,255,255,0.3);
            color: rgba(255,255,255,0.6);
            transition: all 0.3s;
        }}
        .step-dot.active {{
            background: white;
            color: #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        .step-dot.done {{
            background: #4caf50;
            color: white;
        }}

        /* Step content */
        .step-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: none;
        }}
        .step-card.active {{ display: block; }}
        .step-card h2 {{
            color: #1a237e;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }}
        .step-card .step-desc {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }}

        .question-group {{
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #e0e0e0;
        }}
        .question-group:last-of-type {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .question-label {{
            font-weight: 600;
            color: #1a237e;
            font-size: 1rem;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
        }}
        .question-number {{
            background: #1a237e;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            flex-shrink: 0;
            margin-top: 2px;
        }}

        textarea {{
            width: 100%;
            padding: 0.8rem 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 0.95rem;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            transition: border-color 0.2s;
        }}
        textarea:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.2);
        }}

        .radio-group {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
        .radio-option {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .radio-option:hover {{ border-color: #667eea; background: rgba(102,126,234,0.05); }}
        .radio-option input[type="radio"] {{ accent-color: #667eea; }}

        /* Image upload */
        .upload-area {{
            border: 2px dashed #e0e0e0;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            background: #fafafa;
        }}
        .upload-area:hover, .upload-area.dragover {{
            border-color: #667eea;
            background: rgba(102,126,234,0.05);
        }}
        .upload-area .icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .upload-area p {{ color: #666; font-size: 0.9rem; }}
        .upload-area .hint {{ font-size: 0.75rem; color: #999; margin-top: 0.5rem; }}
        .upload-preview {{
            margin-top: 1rem;
            display: none;
        }}
        .upload-preview img {{
            max-width: 100%;
            max-height: 300px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .upload-preview .file-name {{
            font-size: 0.8rem;
            color: #666;
            margin-top: 0.5rem;
        }}
        .paste-hint {{
            font-size: 0.8rem;
            color: #999;
            margin-top: 0.5rem;
        }}

        /* Navigation buttons */
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            margin-top: 1.5rem;
            gap: 1rem;
        }}
        .nav-btn {{
            padding: 0.7rem 2rem;
            border-radius: 99px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            border: none;
        }}
        .nav-btn.prev {{
            background: #e0e0e0;
            color: #666;
        }}
        .nav-btn.prev:hover {{ background: #d0d0d0; }}
        .nav-btn.next {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 2px 10px rgba(102,126,234,0.3);
        }}
        .nav-btn.next:hover {{ transform: translateY(-1px); box-shadow: 0 4px 15px rgba(102,126,234,0.4); }}
        .nav-btn.submit {{
            background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
            color: white;
            box-shadow: 0 2px 10px rgba(76,175,80,0.3);
        }}
        .nav-btn.submit:hover {{ transform: translateY(-1px); }}

        .tip {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 0.8rem 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 1rem;
            font-size: 0.85rem;
            color: #2e7d32;
        }}

        .success-page {{ text-align: center; padding: 3rem 2rem; }}
        .success-icon {{ font-size: 4rem; margin-bottom: 1rem; }}
        .success-page h2 {{ color: #2e7d32; margin-bottom: 0.5rem; }}
        .success-page p {{ color: #666; font-size: 1rem; }}

        @media (max-width: 600px) {{
            body {{ padding: 1rem; }}
            .header, .step-card {{ padding: 1.2rem; }}
            .radio-group {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{description}</p>
            <div class="topic-badge">{topic}</div>
        </div>

        <div class="step-indicators" id="stepIndicators">
            {step_dots}
        </div>

        <form id="mainForm">
            {step_cards}
        </form>
    </div>

    <script>
        let currentStep = 0;
        const totalSteps = {total_steps};
        const steps = document.querySelectorAll('.step-card');
        const dots = document.querySelectorAll('.step-dot');
        const allData = {{}};

        function showStep(n) {{
            steps.forEach((s, i) => {{
                s.classList.toggle('active', i === n);
            }});
            dots.forEach((d, i) => {{
                d.classList.remove('active');
                if (i < n) d.classList.add('done');
                if (i === n) d.classList.add('active');
            }});
            currentStep = n;
        }}

        function nextStep() {{
            // Collect current step data
            const activeStep = steps[currentStep];
            const inputs = activeStep.querySelectorAll('textarea, input[type="radio"]:checked');
            inputs.forEach(inp => {{
                if (inp.type === 'radio') {{
                    if (inp.checked) allData[inp.name] = inp.value;
                }} else {{
                    allData[inp.name] = inp.value;
                }}
            }});

            if (currentStep < totalSteps - 1) {{
                showStep(currentStep + 1);
                window.scrollTo(0, 0);
            }}
        }}

        function prevStep() {{
            if (currentStep > 0) {{
                // Save current data before going back
                const activeStep = steps[currentStep];
                const inputs = activeStep.querySelectorAll('textarea, input[type="radio"]:checked');
                inputs.forEach(inp => {{
                    if (inp.type === 'radio') {{
                        if (inp.checked) allData[inp.name] = inp.value;
                    }} else {{
                        allData[inp.name] = inp.value;
                    }}
                }});
                showStep(currentStep - 1);
                window.scrollTo(0, 0);
            }}
        }}

        function submitForm() {{
            // Collect last step data
            const activeStep = steps[currentStep];
            const inputs = activeStep.querySelectorAll('textarea, input[type="radio"]:checked');
            inputs.forEach(inp => {{
                if (inp.type === 'radio') {{
                    if (inp.checked) allData[inp.name] = inp.value;
                }} else {{
                    allData[inp.name] = inp.value;
                }}
            }});

            // Collect image data
            const imageInputs = document.querySelectorAll('input[type="file"]');
            const imagePromises = [];
            imageInputs.forEach(fileInput => {{
                if (fileInput.files && fileInput.files[0]) {{
                    const promise = new Promise((resolve) => {{
                        const reader = new FileReader();
                        reader.onload = function(e) {{
                            resolve({{
                                id: fileInput.name,
                                name: fileInput.files[0].name,
                                data: e.target.result
                            }});
                        }};
                        reader.readAsDataURL(fileInput.files[0]);
                    }});
                    imagePromises.push(promise);
                }}
            }});

            // Also check for pasted images
            const pasteContainers = document.querySelectorAll('[data-paste-id]');
            pasteContainers.forEach(container => {{
                const img = container.querySelector('img');
                const fileName = container.dataset.fileName || 'pasted_image.png';
                if (img && img.src.startsWith('data:')) {{
                    imagePromises.push(Promise.resolve({{
                        id: container.dataset.pasteId,
                        name: fileName,
                        data: img.src
                    }}));
                }}
            }});

            Promise.all(imagePromises).then(images => {{
                const payload = {{
                    answers: allData,
                    images: images
                }};

                fetch('/submit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }}).then(r => r.json()).then(result => {{
                    if (result.success) {{
                        document.querySelector('.container').innerHTML = `
                            <div class="step-card success-page">
                                <div class="success-icon">✅</div>
                                <h2>提交成功！</h2>
                                <p>你的回答已保存。请回到 CLI 查看生成的答案。</p>
                            </div>
                        `;
                    }}
                }});
            }});
        }}

        // Image upload handlers
        function handleUpload(inputId) {{
            const input = document.getElementById(inputId);
            const preview = document.getElementById(inputId + '_preview');
            const previewImg = preview.querySelector('img');
            const fileName = preview.querySelector('.file-name');

            input.addEventListener('change', function() {{
                if (this.files && this.files[0]) {{
                    const file = this.files[0];
                    const reader = new FileReader();
                    reader.onload = function(e) {{
                        previewImg.src = e.target.result;
                        fileName.textContent = file.name;
                        preview.style.display = 'block';
                    }};
                    reader.readAsDataURL(file);
                }}
            }});
        }}

        // Clipboard paste handler
        function setupPasteHandler(pasteId) {{
            const container = document.querySelector('[data-paste-id="' + pasteId + '"]');
            const hint = container.querySelector('.paste-hint');

            document.addEventListener('paste', function(e) {{
                const items = e.clipboardData.items;
                for (let item of items) {{
                    if (item.type.startsWith('image/')) {{
                        const blob = item.getAsFile();
                        const reader = new FileReader();
                        reader.onload = function(ev) {{
                            let preview = container.querySelector('.upload-preview');
                            if (!preview) {{
                                preview = document.createElement('div');
                                preview.className = 'upload-preview';
                                preview.innerHTML = '<img src="" alt="Pasted image"><div class="file-name"></div>';
                                container.appendChild(preview);
                            }}
                            preview.querySelector('img').src = ev.target.result;
                            preview.querySelector('.file-name').textContent = 'clipboard_image.png';
                            preview.style.display = 'block';
                            container.dataset.fileName = 'clipboard_image.png';
                        }};
                        reader.readAsDataURL(blob);
                        break;
                    }}
                }}
            }});
        }}

        // Init
        showStep(0);
        {init_upload_handlers}
    </script>
</body>
</html>"""


class TopicFormHandler(http.server.BaseHTTPRequestHandler):
    config = None
    answers_file = None
    images_dir = None

    def do_GET(self):
        if self.path == "/" or self.path == "/form":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            config = self.config
            title = config.get("title", "IELTS Coach")
            description = config.get("description", "Please answer the following questions.")
            topic = config.get("topic", "")
            steps = config.get("steps", [])

            # Build step dots
            step_dots = ""
            for i, step in enumerate(steps):
                step_dots += f'<div class="step-dot" data-step="{i}">{i+1}</div>\n'

            # Build step cards
            step_cards = ""
            for i, step in enumerate(steps):
                active = "active" if i == 0 else ""
                step_cards += f'<div class="step-card {active}" data-step="{i}">\n'
                step_cards += f'<h2>{step.get("title", f"Step {i+1}")}</h2>\n'
                step_cards += f'<p class="step-desc">{step.get("description", "")}</p>\n'

                if step.get("tip"):
                    step_cards += f'<div class="tip">{step["tip"]}</div>\n'

                for j, q in enumerate(step.get("questions", []), 1):
                    step_cards += self.render_question(q, j)

                # Navigation buttons
                step_cards += '<div class="nav-buttons">\n'
                if i > 0:
                    step_cards += '<button type="button" class="nav-btn prev" onclick="prevStep()">← 上一步</button>\n'
                else:
                    step_cards += '<div></div>\n'

                if i < len(steps) - 1:
                    step_cards += '<button type="button" class="nav-btn next" onclick="nextStep()">下一步 →</button>\n'
                else:
                    step_cards += '<button type="button" class="nav-btn submit" onclick="submitForm()">✓ 提交所有回答</button>\n'
                step_cards += '</div>\n'
                step_cards += '</div>\n'

            # Build init handlers for image uploads
            init_handlers = ""
            for step in steps:
                for q in step.get("questions", []):
                    if q.get("type") == "image":
                        init_handlers += f"handleUpload('{q['id']}');\n"
                    if q.get("type") == "paste":
                        init_handlers += f"setupPasteHandler('{q['id']}');\n"

            html = FORM_TEMPLATE.format(
                title=title,
                description=description,
                topic=topic,
                step_dots=step_dots,
                step_cards=step_cards,
                total_steps=len(steps),
                init_upload_handlers=init_handlers
            )
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def render_question(self, q, number):
        q_id = q.get("id", f"q{number}")
        q_label = q["label"]
        q_type = q.get("type", "textarea")
        q_placeholder = q.get("placeholder", "")

        html = f'<div class="question-group">\n'
        html += f'<label class="question-label"><span class="question-number">{number}</span>{q_label}</label>\n'

        if q_type == "textarea":
            html += f'<textarea name="{q_id}" placeholder="{q_placeholder}"></textarea>\n'
        elif q_type == "radio":
            options = q.get("options", [])
            html += '<div class="radio-group">\n'
            for opt in options:
                html += f'<label class="radio-option"><input type="radio" name="{q_id}" value="{opt}">{opt}</label>\n'
            html += '</div>\n'
        elif q_type == "image":
            html += f'''<div class="upload-area" onclick="document.getElementById('{q_id}').click()">
                <div class="icon">📁</div>
                <p>点击选择图片，或拖拽图片到此处</p>
                <div class="hint">支持 PNG, JPG 格式</div>
            </div>
            <input type="file" id="{q_id}" name="{q_id}" accept="image/*" style="display:none">
            <div class="upload-preview" id="{q_id}_preview">
                <img src="" alt="Preview">
                <div class="file-name"></div>
            </div>\n'''
        elif q_type == "paste":
            html += f'''<div class="upload-area" data-paste-id="{q_id}">
                <div class="icon">📋</div>
                <p>在此区域按 Ctrl+V 粘贴图片</p>
                <div class="hint">支持从剪贴板粘贴截图</div>
                <div class="paste-hint">或者点击选择本地文件</div>
            </div>
            <input type="file" id="{q_id}" name="{q_id}" accept="image/*" style="display:none">
            <script>
                document.querySelector('[data-paste-id="{q_id}"]').addEventListener('click', function() {{
                    document.getElementById('{q_id}').click();
                }});
                document.getElementById('{q_id}').addEventListener('change', function() {{
                    if (this.files && this.files[0]) {{
                        const reader = new FileReader();
                        reader.onload = function(e) {{
                            let preview = document.querySelector('[data-paste-id="{q_id}"] .upload-preview');
                            if (!preview) {{
                                preview = document.createElement('div');
                                preview.className = 'upload-preview';
                                preview.innerHTML = '<img src="" alt="Preview"><div class="file-name"></div>';
                                document.querySelector('[data-paste-id="{q_id}"]').appendChild(preview);
                            }}
                            preview.querySelector('img').src = e.target.result;
                            preview.querySelector('.file-name').textContent = '{q_id}.png';
                            preview.style.display = 'block';
                        }};
                        reader.readAsDataURL(this.files[0]);
                    }}
                }});
            </script>\n'''

        html += '</div>\n'
        return html

    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                payload = json.loads(post_data.decode("utf-8"))
            except json.JSONDecodeError:
                payload = {"answers": {}, "images": []}

            answers = payload.get("answers", {})
            images = payload.get("images", [])

            # Save answers
            output = {
                "topic": self.config.get("topic", ""),
                "answers": answers,
                "images": []
            }

            # Save images to file
            if images and self.images_dir:
                os.makedirs(self.images_dir, exist_ok=True)
                for img in images:
                    img_id = img.get("id", "image")
                    img_name = img.get("name", f"{img_id}.png")
                    img_data = img.get("data", "")

                    if img_data.startswith("data:"):
                        # Extract base64 data
                        header, data = img_data.split(",", 1)
                        img_bytes = base64.b64decode(data)

                        # Save to file
                        filepath = os.path.join(self.images_dir, img_name)
                        with open(filepath, "wb") as f:
                            f.write(img_bytes)

                        output["images"].append({
                            "id": img_id,
                            "filename": img_name,
                            "path": filepath
                        })
                        print(f"[IMAGE] Saved: {filepath}")

            # Save answers to file
            with open(self.answers_file, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

            print(f"\n[DONE] Answers saved to: {self.answers_file}")
            if output["images"]:
                print(f"[DONE] {len(output['images'])} image(s) saved to: {self.images_dir}")

            # Shutdown server
            threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        pass


def start_server(config_file, answers_file, images_dir, port=DEFAULT_PORT, open_browser=True):
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    TopicFormHandler.config = config
    TopicFormHandler.answers_file = answers_file
    TopicFormHandler.images_dir = images_dir

    server = http.server.HTTPServer(("127.0.0.1", port), TopicFormHandler)

    url = f"http://127.0.0.1:{port}/form"
    print(f"[INFO] Server started: {url}")
    print(f"[INFO] Answers will be saved to: {answers_file}")
    if images_dir:
        print(f"[INFO] Images will be saved to: {images_dir}")
    print(f"[INFO] Waiting for user submission...")

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Server stopped.")


def main():
    parser = argparse.ArgumentParser(description="IELTS Coach Topic Discovery Form Server v2")
    parser.add_argument("--config", required=True, help="Path to config JSON file")
    parser.add_argument("--answers", default="topic_form_answers.json", help="Path to save answers JSON")
    parser.add_argument("--images-dir", default="task1_charts", help="Directory to save uploaded images")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port (default: {DEFAULT_PORT})")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open browser")

    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)

    start_server(args.config, args.answers, args.images_dir, args.port, not args.no_browser)


if __name__ == "__main__":
    main()
