from django.shortcuts import render

# summarize/views.py
import re
from django.http import JsonResponse
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

def extract_video_id(url):
    video_id_match = re.search(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:v\/|embed\/|watch\?v=|watch\?.+&v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return None

def summarize_text(text, max_chunk_length=1000):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = []
    for chunk in chunks:
        input_length = len(chunk.split())  
        max_length = min(300, input_length // 2 + 50)
        summary = summarizer(chunk, max_length=max_length, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return " ".join(summaries)

def summarize_video(request):
    url = request.GET.get('url')
    video_id = extract_video_id(url)

    if video_id:
        transcript = get_video_transcript(video_id)
        if transcript:
            transcript_text = " ".join([segment['text'] for segment in transcript])
            summary_text = summarize_text(transcript_text)
            return JsonResponse({"summary": summary_text})
        else:
            return JsonResponse({"error": "No transcript available."}, status=400)
    else:
        return JsonResponse({"error": "Invalid YouTube URL."}, status=400)
