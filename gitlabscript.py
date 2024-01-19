#!/usr/bin/python3
import json
import csv
import os 
import asyncio
import time
import requests


def getGroups():
    response = requests.get(f'{base_url}/groups', params={'per_page': "100"}, headers={"PRIVATE-TOKEN": pat_token,})
    groups_list = [x['id'] for x in response.json()]
    return groups_list


def getDirectGroupMembers(url_one, url_two, naming):
    group_name = ''
    user_info = ['First_Last Name', 'Username', 'Status', 'Access Level']
    if pat_token and group_id:
        # Get group name
        
        response = requests.get(f'{url_one}', params={'per_page': "100"}, headers={"PRIVATE-TOKEN": pat_token,})
        if response.status_code == 200:
            group_name = ([x['name'] for x in response.json() if x['id']==int(group_id)])
            group_name = f'{group_name[0]}_{naming}'
        
        # Get group members
            response = requests.get(f'{url_two}', params={'per_page': "100"}, headers={"PRIVATE-TOKEN": pat_token,})
            if response.status_code == 200:
                new_list = []
                user_access_level = ''
                for item in response.json():
                    for a_level in access_levels:
                        # print(item['access_level'])
                        if item['access_level'] == int(a_level['id']):
                            user_access_level = a_level['value']

                    new_dict = {'First_Last Name': item['name'], 'Username': item['username'], 'Status': item['state']  , 'Access Level': user_access_level}
                    new_list.append(new_dict)
                
                #Save as CSV file      
                with open(f'{group_name}.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames = user_info)
                    writer.writeheader()
                    writer.writerows(new_list)
                    
                print(f'CSV file saved in current directory as {group_name}.csv')
                    
            else:
                print(f'{response.reason}')
                              
        else:
            print(f'{response.reason}')
        
    else:
        print(f'Enter Access token or Group ID')
        
            
def getDirectProjectMembers():
    
    print(f"""Choose an option
          1. Enter one to get members for a particular group \n
          2. Enter two to get members for all groups""")
    
    user_choice = input('Enter your choice: \n')
    
    if user_choice == str(1):
        pass
    elif user_choice == str(2):
        getGroups()
    
    groups_list = getGroups()
    
    if groups_list:

        for group in groups_list:
            
            if pat_token:
                url_one = f'{base_url}/groups/{group}/projects'
                # Get group name
                response = requests.get(f'{base_url}/groups/{group}', params={'per_page': "100"}, headers={"PRIVATE-TOKEN": pat_token,})
                if response.status_code == 200:
                    group_name = response.json()['name']
                    
                    print(f'The group name is {group_name}')                    
                    print(f'Getting list of project ids for {group_name} group...')
                    
                    response = requests.get(f'{url_one}', params={'per_page': "100"}, headers={"PRIVATE-TOKEN": pat_token,})
                    if response.status_code == 200:
                        # Grab list of project ids
                        project_ids = ([x['id'] for x in response.json()])
                        print(f'{project_ids}')
                        
                        for project_id in project_ids:
                            url_two = f'{base_url}/projects/{project_id}/members/all'
                            naming = f'All_Members'
                        
                        # Loop through list and create csvs
                            project_name = ''
                            user_info = ['First_Last Name', 'Username', 'Status', 'Access Level']
                                
                            # Get project name
                            print(f'Getting project name...')
                            response = requests.get(f'{url_one}', params={'per_page': "100"}, headers={"PRIVATE-TOKEN": pat_token,})
                            if response.status_code == 200:
                                project_name = ([x['name'] for x in response.json() if x['id']==int(project_id)])
                                project_name = f'{project_name[0]}_{naming}'
                            
                            # Get project members
                                print(f'Getting project members for {project_name}')
                                response = requests.get(f'{url_two}', params={'per_page': "100"}, headers={"PRIVATE-TOKEN": pat_token,})
                                if response.status_code == 200:
                                    new_list = []
                                    user_access_level = ''
                                    for item in response.json():
                                        for a_level in access_levels:
                                            if item['access_level'] == int(a_level['id']):
                                                user_access_level = a_level['value']

                                        new_dict = {'First_Last Name': item['name'], 'Username': item['username'], 'Status': item['state']  , 'Access Level': user_access_level}
                                        new_list.append(new_dict)
                                    
                                    #Save as CSV file      
                                    with open(f'{save_directory}/{project_name}.csv', 'w') as csvfile:
                                        writer = csv.DictWriter(csvfile, fieldnames = user_info)
                                        writer.writeheader()
                                        writer.writerows(new_list)
                                        
                                    print(f'CSV file saved in {save_directory} as {group_name}_Group_{project_name}.csv')
                                    
                                    time.sleep(2)
                                        
                                else:
                                    print(f'{response.reason}')
                                    break
                                                
                            else:
                                print(f'{response.reason}')
                                break
                                
                            # else:
                            #     print(f'Enter Access token or Group ID')
                            #     break
                    
                        # group_name = f'{group_name[0]}_{naming}'
        else:
            print(f'Enter Access token or Group ID')

    else:
        print(f'No groups exist')
            
                


# Call main function
if __name__ == "__main__":
    
    print(f"""Select one of the four options \n
      1. Get direct GROUP members \n
      2. Get ALL GROUP members including inherited and invited members \n
      3. Get direct PROJECT members \n
      4. Get ALL PROJECT members including inherited and invited members \n
      """)    

    group_id = '31'
    project_id = ''
    user_id = ''
    working_directory = os.getcwd()
    save_directory = f'{working_directory}/csv_files'
    pat_token = 'glpat-xxxxxx-xxxxxxxxxx'
    
    if os.path.exists(f'{working_directory}/csv_files'):
        pass
    else:
        os.mkdir('csv_files')

    # Constant variables
    
    access_levels = [
      { "id": "50", "value": "Owner" },
      { "id": "40", "value": "Maintainer Access" },
      { "id": "30", "value": "Developer Access" },
      { "id": "20", "value": "Reporter Access" },
      { "id": "10", "value": "Guest Access" },
      { "id": "5", "value": "Minimal Access" },
      { "id": "0", "value": "No Access" },
    ]
    base_url = "https://gitlab-lin5.lvmh.lbn.fr/api/v4"
    # delimiter = "?per_page="+requests_per_page
    
    user_choice = input('Enter your choice: \n')
    
    if user_choice == str(1):
        url_one = f'{base_url}/groups'
        url_two = f'{base_url}/groups/{group_id}/members'
        naming = f'Direct_Members'
        getDirectGroupMembers(url_one, url_two, naming)
        
    elif user_choice == str(2):
        url_one = f'{base_url}/groups'
        url_two = f'{base_url}/groups/{group_id}/members/all'
        naming = f'All_Members'
        getDirectGroupMembers(url_one, url_two, naming)
        
    elif user_choice == str(3):
        url_one = f'{base_url}/{group_id}projects'
        
        getDirectProjectMembers()
        
    elif user_choice == str(4):
        url_one = f'{base_url}/projects'
        url_two = f'{base_url}/projects/{project_id}/members/all'
        naming = f'All_Members'
        getDirectProjectMembers(url_one, url_two, naming)
        
    else:
        print(f"Choose a valid option")
