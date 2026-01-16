from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ReadingSession, AnalysisResult
from .services import analyze_audio_with_gemini

class AnalyzeReadingView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        print("📥 Received Audio for Analysis...")
        
        # 1. Extract Data
        audio_file = request.FILES.get('audio')
        user_id = request.data.get('user_id', 'anon')
        expected_text = request.data.get('expected_text', "Default text")
        
        # CRITICAL: Receive the age group from the previous model/frontend
        # Default to '8-10 years' if missing, but it should be passed!
        age_group = request.data.get('age_group', '8-10 years') 

        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)

        # 2. Save Session Locally
        session = ReadingSession.objects.create(
            user_id=user_id,
            session_id=f"sess_{request.data.get('session_id', '001')}",
            audio_file=audio_file,
            expected_text=expected_text
        )

        try:
            # 3. Call AI Service with Age Group
            ai_data = analyze_audio_with_gemini(
                session.audio_file.path, 
                expected_text,
                age_group
            )
            
            if not ai_data:
                return Response({"error": "AI analysis failed"}, status=500)

            # 4. Save Results to DB
            AnalysisResult.objects.create(
                session=session,
                transcribed_text=ai_data.get('assessment_summary', ''), # Storing summary here for now
                accuracy_score=ai_data.get('accuracy_score', 0),
                wpm=ai_data.get('reading_speed_wpm', 0),
                mispronunciations=ai_data.get('struggle_words', []),
                risk_score="High" if ai_data.get('risk_flag') else "Low",
                feedback=ai_data.get('recommended_solution', '') # <--- The Age-Based Solution
            )

            # 5. Return JSON to Frontend
            return Response({
                "status": "success",
                "analysis": ai_data
            })

        except Exception as e:
            print(f"❌ Server Error: {e}")
            return Response({"error": str(e)}, status=500)