"""
Module for generating mock news articles for the Mackney Gazette.
"""
import os
import yaml
import json
import random
import datetime
import pandas as pd
from pathlib import Path

def load_config(config_file):
    """
    Load configuration from YAML file.
    
    Args:
        config_file: Path to the YAML configuration file
        
    Returns:
        Dict containing configuration data
    """
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def load_town_data(file_path):
    """
    Load town data from a JSON file.
    
    Args:
        file_path: Path to the town data JSON file
        
    Returns:
        Dict containing town data
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading town data: {e}")
        return {}
        
def load_people_data(file_path):
    """
    Load people data from a CSV file.
    
    Args:
        file_path: Path to the people data CSV file
        
    Returns:
        DataFrame containing people data
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading people data: {e}")
        return pd.DataFrame()

def create_new_story():
    """
    Create a new news story by sampling category and author from configuration.
    The story will be saved to articles.csv.
    
    Returns:
        Dict containing the generated article data
    """
    # Get the directory of the current file
    current_dir = Path(__file__).parent
    data_dir = Path(current_dir).parent.parent.parent / 'data'
    
    # Load configuration
    config_file = current_dir / 'article_config.yaml'
    config = load_config(config_file)
    
    # Load town and people data
    town_data_file = data_dir / 'town_data.json'
    people_data_file = data_dir / 'people_data.csv'
    
    town_data = load_town_data(town_data_file)
    people_data = load_people_data(people_data_file)
    
    # Sample category
    category = random.choice(config['categories'])
    
    # Find authors who specialize in this category if possible
    category_authors = [
        author for author in config['authors'] 
        if category in author.get('specialties', [])
    ]
    
    # If no author specializes in this category, choose any author
    if not category_authors:
        author_info = random.choice(config['authors'])
    else:
        # Higher chance (70%) of selecting an author specialized in this category
        if random.random() < 0.7:
            author_info = random.choice(category_authors)
        else:
            author_info = random.choice(config['authors'])
    
    # Extract author name and persona
    author_name = author_info['name']
    author_persona = author_info['persona']
    author_style = author_info['writing_style']
    
    # Generate article ID (timestamp-based for uniqueness)
    article_id = f"ART-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Sample data from town and people based on article_seed
    article_town_data = {}
    article_people_data = []
    
    print(f"\n--- GENERATING ARTICLE {article_id} ---")
    print(f"Category: {category}")
    print(f"Author: {author_name} ({author_info['writing_style']})")
    
    # Sample town data if available and according to article_seed
    if town_data and 'article_seed' in config and 'town_data' in config['article_seed']:
        town_config = config['article_seed']['town_data']
        
        # Check if we should include town data based on inclusion probability
        if random.random() < town_config.get('inclusion_probability', 0.5):
            print(f"\n=== TOWN DATA SAMPLING ===")
            print(f"Town: {town_data.get('name', 'Unknown')}")
            print(f"Population: {town_data.get('population', 0)}")
            print(f"Founded: {town_data.get('founded_year', 'Unknown')}")
            print(f"Climate: {town_data.get('climate', 'Unknown')}")
            
            # Extract relevant town features based on feature weights
            feature_weights = town_config.get('feature_weights', {})
            article_town_data = {
                'town_name': town_data.get('name', ''),
                'town_population': town_data.get('population', 0),
                'town_features': {}
            }
            
            # Sample streets
            sampled_streets = []
            if 'streets' in town_data and 'streets' in feature_weights:
                street_config = feature_weights['streets']
                if random.random() < street_config.get('probability', 0.5):
                    max_streets = street_config.get('max_count', 3)
                    num_streets = min(max_streets, len(town_data['streets']))
                    if num_streets > 0:
                        sampled_streets = random.sample(town_data['streets'], num_streets)
                        article_town_data['town_features']['streets'] = sampled_streets
                        
                        print(f"\nSampled Streets (max: {max_streets}):")
                        for street in sampled_streets:
                            print(f"  - {street.get('name', 'Unknown Street')} ({street.get('type', 'Unknown Type')})")
            
            # Sample landmarks if present
            sampled_landmarks = []
            if 'landmarks' in town_data and 'landmarks' in feature_weights:
                landmark_config = feature_weights['landmarks']
                if random.random() < landmark_config.get('probability', 0.5):
                    max_landmarks = landmark_config.get('max_count', 2)
                    num_landmarks = min(max_landmarks, len(town_data.get('landmarks', [])))
                    if num_landmarks > 0:
                        sampled_landmarks = random.sample(town_data['landmarks'], num_landmarks)
                        article_town_data['town_features']['landmarks'] = sampled_landmarks
                        
                        print(f"\nSampled Landmarks (max: {max_landmarks}):")
                        for landmark in sampled_landmarks:
                            print(f"  - {landmark.get('name', 'Unknown Landmark')} ({landmark.get('type', 'Unknown Type')})")
                            print(f"    Located on: {landmark.get('street', 'Unknown Street')}")
                            print(f"    Established: {landmark.get('established_year', 'Unknown')}")
            
            # Sample businesses if present
            sampled_businesses = []
            if 'businesses' in town_data and 'businesses' in feature_weights:
                business_config = feature_weights['businesses']
                if random.random() < business_config.get('probability', 0.5):
                    max_businesses = business_config.get('max_count', 3)
                    num_businesses = min(max_businesses, len(town_data.get('businesses', [])))
                    if num_businesses > 0:
                        sampled_businesses = random.sample(town_data['businesses'], num_businesses)
                        article_town_data['town_features']['businesses'] = sampled_businesses
                        
                        print(f"\nSampled Businesses (max: {max_businesses}):")
                        for business in sampled_businesses:
                            print(f"  - {business.get('name', 'Unknown Business')} ({business.get('type', 'Unknown Type')})")
                            print(f"    Located on: {business.get('street', 'Unknown Street')}")
                            print(f"    Founded: {business.get('founded_year', 'Unknown')}")
                            
            # Sample events if present
            sampled_events = []
            if 'events' in town_data and 'events' in feature_weights:
                event_config = feature_weights['events']
                if random.random() < event_config.get('probability', 0.5):
                    max_events = event_config.get('max_count', 2)
                    num_events = min(max_events, len(town_data.get('events', [])))
                    if num_events > 0:
                        sampled_events = random.sample(town_data['events'], num_events)
                        article_town_data['town_features']['events'] = sampled_events
                        
                        print(f"\nSampled Events (max: {max_events}):")
                        for event in sampled_events:
                            print(f"  - {event.get('name', 'Unknown Event')} ({event.get('type', 'Unknown Type')})")
                            print(f"    Date: {event.get('date', 'Unknown Date')}")
                            print(f"    Location: {event.get('location', 'Unknown Location')}")
    
    # Sample people data if available and according to article_seed
    if not people_data.empty and 'article_seed' in config and 'people_data' in config['article_seed']:
        people_config = config['article_seed']['people_data']
        
        # Check if we should include people data based on inclusion probability
        if random.random() < people_config.get('inclusion_probability', 0.5):
            print(f"\n=== PEOPLE DATA SAMPLING ===")
            
            # Determine how many people to include
            min_people = people_config.get('min_people_per_article', 1)
            max_people = people_config.get('max_people_per_article', 3)
            num_people = random.randint(min_people, max_people)
            print(f"Target number of people to include: {num_people}")
            
            # Sample people
            if len(people_data) > 0:
                # Apply demographic filters if specified
                filtered_people = people_data
                chosen_age_group = "All ages"
                
                # Filter by age groups if specified
                if 'demographic_weights' in people_config and 'age' in people_config['demographic_weights']:
                    age_weights = people_config['demographic_weights']['age']
                    
                    # Choose an age group based on weights
                    age_groups = list(age_weights.keys())
                    age_probs = list(age_weights.values())
                    chosen_age_group = random.choices(age_groups, weights=age_probs, k=1)[0]
                    print(f"Selected age group: {chosen_age_group}")
                    
                    # Apply age filter
                    if chosen_age_group == "18-30":
                        filtered_people = people_data[(people_data['age'] >= 18) & (people_data['age'] <= 30)]
                    elif chosen_age_group == "31-50":
                        filtered_people = people_data[(people_data['age'] >= 31) & (people_data['age'] <= 50)]
                    elif chosen_age_group == "51-70":
                        filtered_people = people_data[(people_data['age'] >= 51) & (people_data['age'] <= 70)]
                    elif chosen_age_group == "71+":
                        filtered_people = people_data[people_data['age'] >= 71]
                
                # Sample from filtered people
                if not filtered_people.empty:
                    sample_size = min(num_people, len(filtered_people))
                    sampled_people = filtered_people.sample(sample_size)
                    article_people_data = sampled_people.to_dict('records')
                    
                    print(f"\nSampled {len(article_people_data)} people:")
                    for i, person in enumerate(article_people_data):
                        print(f"\nPerson {i+1}:")
                        print(f"  Name: {person.get('first_name', '')} {person.get('last_name', '')}")
                        print(f"  Age: {person.get('age', 'Unknown')}")
                        print(f"  Occupation: {person.get('occupation', 'Unknown')}")
                        print(f"  Location: {person.get('location', 'Unknown')}")
                        print(f"  Temperament: {person.get('temperament_type', 'Unknown')} - {person.get('temperament_description', 'Unknown')}")
                else:
                    print("No people matched the demographic filters.")
    
    # Create article with minimal data for now
    article = {
        'article_id': article_id,
        'title': f"Placeholder Title for {category} Article",
        'slug': f"placeholder-title-for-{category.lower().replace(' ', '-')}-article",
        'body': "This is a placeholder for the article body.",
        'summary': "This is a placeholder summary.",
        'publication_date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'author': author_name,
        'author_persona': author_persona,
        'author_style': author_style,
        'category': category,
        'status': 'Draft',
        'story_status': 'Ongoing',
    }
    
    # Define the path to the CSV file in the data directory
    csv_file = Path(current_dir).parent.parent.parent / 'data' / 'articles.csv'
    
    # Check if the file exists
    file_exists = csv_file.is_file()
    
    # Define expected columns for the DataFrame
    expected_columns = [
        'article_id', 'title', 'slug', 'body', 'summary', 
        'publication_date', 'last_updated', 'author', 
        'author_persona', 'author_style', 'category', 
        'status', 'story_status', 'town_data', 'people_data'
    ]
    
    # Convert the article dictionary to a DataFrame
    article_df = pd.DataFrame([article])
    
    if file_exists:
        try:
            # Try to read the existing CSV file
            existing_df = pd.read_csv(csv_file)
            
            # Check if the columns match
            if set(existing_df.columns) != set(expected_columns):
                print("CSV structure has changed. Creating backup and new file...")
                
                # Create a backup
                backup_file = f"{csv_file}.bak"
                import shutil
                shutil.copy2(csv_file, backup_file)
                
                # Ensure all columns are present in both DataFrames
                for col in expected_columns:
                    if col not in existing_df.columns:
                        existing_df[col] = ""
                
                # Reorder and filter columns to match expected structure
                existing_df = existing_df[expected_columns]
                
                # Concatenate with the new article and save
                updated_df = pd.concat([existing_df, article_df], ignore_index=True)
                updated_df.to_csv(csv_file, index=False)
            else:
                # Append the new article
                article_df.to_csv(csv_file, mode='a', header=False, index=False)
                
        except pd.errors.EmptyDataError:
            # File exists but is empty
            article_df.to_csv(csv_file, index=False)
            
        except Exception as e:
            # Handle other errors (like permission issues)
            print(f"Error processing CSV file: {e}")
            # Try writing new file
            article_df.to_csv(csv_file, index=False)
    else:
        # File doesn't exist, create it
        article_df.to_csv(csv_file, index=False)
    
    print(f"Created new article with ID: {article_id}")
    return article

if __name__ == "__main__":
    create_new_story()
