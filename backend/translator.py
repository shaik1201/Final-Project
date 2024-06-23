from deep_translator import GoogleTranslator
import re

def translateLocation(job_data):
    for idx, job in enumerate(job_data):
        job_location = job['location']
        new_job_location = None
        if job_location:
            # Split by comma, 'or', 'and', '/', etc.
            parts = re.split(r', | or | and | / | \(|\)', job_location)
            for part in parts:
                clean_part = part.strip()
                if clean_part and "מחוז" not in clean_part:
                    new_job_location = str(clean_part)
                    break

        if new_job_location == 'רעננה':
            translated_location = 'Raanana'
        elif new_job_location == 'מגדל':
            translated_location = 'Migdal HaEmeq'
        else:
            translated_location = GoogleTranslator(source='iw', target='en').translate(new_job_location)
        job_data[idx]['location'] = translated_location

    return job_data


