# modules/extraction.py
import os
from openai import OpenAI

# Load the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it to use OpenAI API.")

client = OpenAI(api_key=api_key)

def extract_exercises_from_transcript(transcript_file: str, output_dir: str = "yt_video_exercises_routine") -> str:
    try:
        # Read the transcript from the file
        with open(transcript_file, "r") as file:
            transcript = file.read()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a secetary and a personal trainer, who has multitude of experience in both forming routines/schedules and with exersises"},
                {"role": "user","content": f"Given is a trascript of a youtube video about exersising. From this video I want you as my secetary to create the esxersise routine according to the recomendation provided by the narator in the video. \nSpecify what order i need to perfrom the exersies in, for how many sets each, and how many repetetions in a given set. Further sepcify about the rest time i should have/maintain in-between the sets. \nFurther-more provide me with any other special notes i need to know about the specific exersise or just the workout routine in general. \nProvide me the routine in the following JSON format -- \nExercise: <Exercise Name> \n\t- Sets: <Number of Sets> \n\t- Repetitions: <Number of Reps> \n\t- Duration: <Duration if mentioned> \n\t- Notes: <Special notes for the exersise> \nTranscript: \n{transcript}"}
            ]
        )

        # Extract the text from the response
        extracted_routine = response.choices[0].message.content
        
        # # Parse the extracted routine as JSON
        # try:
        #     routine_data = json.loads(response)
        # except json.JSONDecodeError:
        #     raise ValueError("Failed to parse the response as JSON. Please check the prompt and response format.")
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Create a filename for the output file based on the transcript filename
        base_filename = os.path.splitext(os.path.basename(transcript_file))[0].replace("_transcript", "")
        output_filename = f"{base_filename}_routine.txt"
        output_path = os.path.join(output_dir, output_filename)

        # Save the extracted routine to the specified directory in JSON format
        with open(output_path, "w") as f:
            f.write(extracted_routine)
        
        # Return the path of the saved routine file
        return output_path
    
    except Exception as e:
        raise ValueError(f"Failed to extract workout routine: {e}")
    
    