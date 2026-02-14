"""
Generate mock dataset for career recommendation training
"""
import pandas as pd
import numpy as np
import random
from pathlib import Path

# Career categories and careers
CAREER_CATEGORIES = {
    'STEM': ['Data Scientist', 'Software Engineer', 'AI Engineer', 'Cybersecurity Analyst', 'Biomedical Engineer', 'Mechanical Engineer', 'Electrical Engineer'],
    'Business': ['Business Analyst', 'Financial Analyst', 'Marketing Manager', 'Operations Manager', 'Consultant', 'Investment Banker'],
    'Healthcare': ['Doctor', 'Nurse', 'Pharmacist', 'Physical Therapist', 'Medical Researcher'],
    'Education': ['Teacher', 'Professor', 'Educational Administrator', 'Curriculum Developer'],
    'Arts': ['Graphic Designer', 'Writer', 'Musician', 'Film Director', 'Architect'],
    'Social': ['Social Worker', 'Psychologist', 'Counselor', 'Human Resources Manager'],
}

# Skills mapping
TECHNICAL_SKILLS = ['Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning', 'Data Analysis', 'Web Development', 'Mobile Development', 'Cloud Computing', 'Statistics']
SOFT_SKILLS = ['Communication', 'Leadership', 'Problem Solving', 'Teamwork', 'Critical Thinking', 'Creativity', 'Time Management']

# Holland Code types
HOLLAND_CODES = ['R', 'I', 'A', 'S', 'E', 'C']  # Realistic, Investigative, Artistic, Social, Enterprising, Conventional

def generate_student_record():
    """Generate a single student-career record"""
    # Academic features
    gpa = round(random.uniform(2.5, 4.0), 2)
    degree_level = random.choice(['Bachelor\'s', 'Master\'s', 'PhD'])
    
    # Skills
    num_tech_skills = random.randint(2, 6)
    technical_skills = random.sample(TECHNICAL_SKILLS, num_tech_skills)
    num_soft_skills = random.randint(2, 5)
    soft_skills = random.sample(SOFT_SKILLS, num_soft_skills)
    
    # Interests
    interests = random.sample(['Technology', 'Research', 'Business', 'Arts', 'Healthcare', 'Education'], random.randint(2, 4))
    
    # Personality
    holland_code = ''.join(random.sample(HOLLAND_CODES, 3))
    
    # Academic field
    academic_field = random.choice(['Computer Science', 'Engineering', 'Business', 'Medicine', 'Arts', 'Education', 'Social Sciences'])
    
    # Determine career based on features (simplified logic)
    if gpa >= 3.5 and 'Python' in technical_skills and 'Machine Learning' in technical_skills:
        career_category = 'STEM'
        career = random.choice(CAREER_CATEGORIES['STEM'][:3])  # Top STEM careers
    elif gpa >= 3.3 and academic_field == 'Business':
        career_category = 'Business'
        career = random.choice(CAREER_CATEGORIES['Business'])
    elif academic_field == 'Medicine':
        career_category = 'Healthcare'
        career = random.choice(CAREER_CATEGORIES['Healthcare'])
    elif 'I' in holland_code and 'Research' in interests:
        career_category = 'STEM'
        career = random.choice(['Data Scientist', 'AI Engineer', 'Medical Researcher'])
    else:
        # Random career
        career_category = random.choice(list(CAREER_CATEGORIES.keys()))
        career = random.choice(CAREER_CATEGORIES[career_category])
    
    return {
        'gpa': gpa,
        'degree_level': degree_level,
        'academic_field': academic_field,
        'technical_skills': technical_skills,
        'soft_skills': soft_skills,
        'interests': interests,
        'holland_code': holland_code,
        'career': career,
        'career_category': career_category,
    }

def generate_dataset(n_records=1000, output_path='career_dataset.csv'):
    """Generate dataset with n_records"""
    records = [generate_student_record() for _ in range(n_records)]
    df = pd.DataFrame(records)
    
    # Expand skills and interests into binary features
    all_tech_skills = set()
    all_soft_skills = set()
    all_interests = set()
    
    for record in records:
        all_tech_skills.update(record['technical_skills'])
        all_soft_skills.update(record['soft_skills'])
        all_interests.update(record['interests'])
    
    # Create binary features
    for skill in all_tech_skills:
        df[f'has_{skill.lower().replace(" ", "_")}'] = df['technical_skills'].apply(lambda x: 1 if skill in x else 0)
    
    for skill in all_soft_skills:
        df[f'has_{skill.lower().replace(" ", "_")}'] = df['soft_skills'].apply(lambda x: 1 if skill in x else 0)
    
    for interest in all_interests:
        df[f'interest_{interest.lower().replace(" ", "_")}'] = df['interests'].apply(lambda x: 1 if interest in x else 0)
    
    # Encode degree level
    degree_mapping = {'Bachelor\'s': 1, 'Master\'s': 2, 'PhD': 3}
    df['degree_level_encoded'] = df['degree_level'].map(degree_mapping)
    
    # Encode Holland Code (simplified - count occurrences of each type)
    for code in HOLLAND_CODES:
        df[f'holland_{code}'] = df['holland_code'].apply(lambda x: x.count(code))
    
    # Save to CSV
    output_file = Path(__file__).parent / output_path
    df.to_csv(output_file, index=False)
    print(f"Generated dataset with {n_records} records saved to {output_file}")
    
    return df

if __name__ == '__main__':
    generate_dataset(n_records=1000)

