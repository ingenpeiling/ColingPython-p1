import requests
import json
import sys
from collections import defaultdict

class GitHubUser:
    def __init__(self, username):
        self.username = username
        self.base_url = f"https://api.github.com/users/{username}"

## basic_data - для извлечения информации о числе подписчиков и числе репозиториев,
## repos_data - для извлечения названий и описаний репозиториев и используемых языков
                
        basic_data = requests.get(self.base_url).json()
        repos_data = requests.get(self.base_url + '/repos?page=1&per_page=1000').json()
        
        self.repos_data = repos_data
        self.basic_data = basic_data
        
    def num_repos(self):
        result = self.basic_data['public_repos']
        return result
        
    def repos_desc(self):
        print('Here are all the repositories of this user: \n')
        for i in range(len(self.repos_data)):
            name = self.repos_data[i]['full_name']
            description = self.repos_data[i]['description']            
            print(name, '\n', description)
        print('\n')
            
    def languages(self, to_print=False):
        lang_dict = defaultdict(int)
        for i in range(len(self.repos_data)):
            language = self.repos_data[i]['language']
            lang_dict[language] += 1
        if to_print == True:
            print('Here are the languages this user prefers: \n')
            for lang in lang_dict:
                print(f'{lang}: {lang_dict[lang]} repositories.')
            print('\n')
        else:
            return lang_dict
    
    def followers(self):
        result = self.basic_data["followers"]
        return result

    

# это попытка сократить число запросов к серверу: сначала создать объект GitHubUser для каждого пользователя из списка, а в последующих функциях
# обращаться к этому списку. но даже при этом после нескольких попыток оказывается, что исчерпан лимит обращений к серверу. возможно, можно сделать еще что-то?
def cash(userlist):
    result = []
    for user in userlist:
        x = GitHubUser(user)
        result.append(x)
    return result
    
def most_repos(cashed_userlist):
    final = {}
    for user in cashed_userlist:
        num = user.num_repos()
        final[user] = num
    result = max(final, key=final.get)
    print(f'{result.username} has the most repositories: {final[result]} \n')

def pop_lang(cashed_userlist):
    final_dict = defaultdict(int)
    for user in cashed_userlist:
        user_langs = user.languages()
        for lang in user_langs:
            final_dict[lang] += user_langs[lang]
    result = max(final_dict, key=final_dict.get)
    print(f'The most popular language among these users is {result}, it is used in {final_dict[result]} repositories. \n')
    
def most_followers(cashed_userlist):
    final = {}
    for user in cashed_userlist:
        num = user.followers()
        final[user] = num
    result = max(final, key=final.get)
    print(f'{result.username} has the most followers: {final[result]}')
        

def main():
    userlist = sys.argv[1:]
    username = input('Choose one user. ')
    chosen = GitHubUser(username)
    chosen.repos_desc()
    chosen.languages(to_print=True)

    cashed = cash(userlist)
    most_repos(cashed)
    pop_lang(cashed)
    most_followers(cashed)

if __name__ == "__main__":
    main()
