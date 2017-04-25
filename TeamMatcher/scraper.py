import urllib.request as urllib
import re
import json
import pymysql
import string


from bs4 import BeautifulSoup

db = None
dbc = None
try:
    db = pymysql.connect(host='localhost', port=3310, user='admin', passwd='admin', db='teammatcher$TeamMatcher', charset='utf8')
    db.set_character_set('utf8')

except:
   print('Unable to connect!')


sp2017 = "https://wiki.illinois.edu/wiki/display/cs411sp17/CS411+Spring+2017+Project+Teams"
team20 = "https://wiki.illinois.edu/wiki/display/cs411sp17/Team+20"

count = 0

projects = []

class Project:
    def __init__(self, name, desc, members, skills):
        self.name = name
        self.desc = desc
        self.members = members
        self.skills = skills

    def get_members(self): # return members
        return self.members

    def get_desc(self): # return description
        return self.desc

    def get_name(self): # return name
        return self.name

    def get_skills(self): # return skills
        return self.skills


def scrape_project_list(page):
    """
    Scrape links to project pages
    :param page: 
    :return: 
    """
    try:
        open_page = urllib.urlopen(page)
    except:
        return
    soup = BeautifulSoup(open_page, "html.parser")

    links = soup.find('table').find_next('table').find_all_next('a', href=re.compile(r'/cs411sp17/'))[2:]
    for a in links:
        link = a['href']
        if link.startswith("http") is False:
            link = "https://wiki.illinois.edu" + link
        print(link)
        scrape_page(link)

def scrape_page(page):
    """ 
    Scrape project title, descrption, members
    :param page
    :return name, age
    """
    try:
        open_page = urllib.urlopen(page)
    except:
        return

    global count
    soup = BeautifulSoup(open_page, "html.parser")

    name_soup = soup.find(string=re.compile('project title', re.I)).find_parent(['td','th']).next_sibling
    name = name_soup.find_next(string=True)

    desc_soup = soup.find('a', string=re.compile(r'escription'))
    if desc_soup is None:
        return None
    link = desc_soup['href']
    if link.startswith("http") is False:
        link = "https://wiki.illinois.edu" + link
    desc = scrape_description(link)

    print('stuck')
    skill_soup = soup.find('a', string=re.compile(r'plan', re.I))
    if skill_soup is None:
        return None
    skill_link = skill_soup['href']
    if skill_link.startswith("http") is False:
        skill_link = "https://wiki.illinois.edu" + skill_link
    skills = scrape_skills(skill_link)

    members_soup = soup.find(string="Members").find_parent(['td','th'])
    members = str(members_soup.find_next(['td','th']).find_all(string=True))
    members = "".join(members)
    transtab = str.maketrans("", "","'<>[]")
    members = members.translate(transtab).split(',')
    i = 0
    for member in members:
        members[i] = member.strip(' (@\\')
        i+=1

    members = [x for x in members if len(x) > 4 and 'illinois' not in x]


    if desc is None or members is None or name is None:
        return
    projects.insert(0, Project(name, desc, members, skills))
    print('From link '+ desc_soup['href']+':')
    print(' Title: '+ name)
    print(' Description: ' + desc)
    print(members)
    print(skills)
    count+=1
    print(count)

def scrape_description(page):
    """
    Scrape description page to obtain description.
    :param page: 
    :return: text of descriptions
    """
    try:
        open_page = urllib.urlopen(page)
    except:
        return
    soup = BeautifulSoup(open_page, "html.parser")
    soup = soup.find('div', {'class':'wiki-content'})
    if soup is None:
        return None
    return soup.get_text()

def scrape_skills(page):

    try:
        open_page = urllib.urlopen(page)
    except:
        return
    soup = BeautifulSoup(open_page, "html.parser")
    soup = soup.find('div', {'class':'wiki-content'})
    if soup is None:
        return None
    desc = soup.get_text().lower()

    skills = ['php','java','c++','flask','python', 'js', 'javascript', 'ajax', 'ruby', 'html', 'css', 'c#', 'visual basic', 'vb', 'perl', 'swift', 'objective-c', 'mysql', 'pgsql', 'jquery', 'nodejs', 'mongodb', 'cpanel', 'github', 'git', 'android', 'ionic', 'ios', 'django']
    ret = []
    for skill in skills:
        if desc.find(skill) != -1:
            ret.insert(0, skill)
    return ret

def write_to_json():
    data = []
    for node in projects:
        data.append(node.__dict__)
    with open('projects.json', 'w') as json_file:
        json.dump(data, json_file)

def projects_from_json():

    with open('projects.json') as json_file:
        data = json.load(json_file)
        for p in data:
            x = Project(p['name'], p['desc'], p['members'], p['skills'])
            projects.insert(0,x)


def write_to_sql(db):
    cur = db.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    for node in projects:
        for member in node.get_members():
            cur.execute("""
                INSERT INTO Student(
                  Name,
                  GPA,
                  School, 
                  Major, 
                  Year, 
                  Email,
                  Likes,
                  Password
                )
                VALUES(%s, 3.0, %s, %s, 3, %s, 0, %s)
            """, (
                member,
                'UIUC',
                'CS',
                member,
                '1234'
            ))
        name = node.get_name()
        print(name)
        desc = node.get_desc()
        cur.execute("""
                    INSERT INTO Project(
                        Name,
                        Description,
                        Max_Capacity,
                        Status,
                        CreatedByStudentId
                    )
                    VALUES(%s, %s, 4, %s,
                        (SELECT Student_Id FROM Student WHERE Email=%s LIMIT 1))
                    
                """, (name,
                      desc,
                      'Created',
                      node.get_members()[0]))
        if node.get_skills() is not None:
            for skill in node.get_skills():
                cur.execute("""
                    INSERT IGNORE INTO Skill (Name) 
                    VALUES (%s) 
                """, (skill
                ))
                cur.execute("""
                    INSERT INTO ProjectNeedsSkill(
                      Project_Id,
                      Skill_Id
                    )
                    VALUES((SELECT Project_Id FROM Project WHERE Name = %s LIMIT 1), (SELECT Skill_Id FROM Skill WHERE Name= %s LIMIT 1))
                """, (name,
                      skill
                ))
        for member in node.get_members():
            cur.execute("""
                INSERT INTO StudentPartOfProject(
                  Student_Id,
                  Project_Id
                )
                VALUES((SELECT Student_Id FROM Student WHERE Email= %s LIMIT 1) , (SELECT Project_Id FROM Project WHERE Name = %s LIMIT 1))
            """, (member,
                  name
            ))
            if node.get_skills() is not None:
                for skill in node.get_skills():
                    cur.execute("""
                        INSERT INTO StudentHasSkill(
                          Student_Id,
                          Skill_Id,
                          Skill_Level
                        )
                        VALUES((SELECT Student_Id FROM Student WHERE Email= %s LIMIT 1) , (SELECT Skill_Id FROM Skill WHERE Name = %s LIMIT 1), 2)
                    """, (member,
                          skill,
                    ))

        db.commit()


#scrape_project_list(sp2017)
#write_to_json()
projects_from_json()
write_to_sql(db)

