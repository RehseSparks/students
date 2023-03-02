from bs4 import BeautifulSoup
import requests

class course:
    name = ""
    url = ""
    def add_name(self, input):
        self.name = input
    def add_url(self, input):
        self.url = input
    def get_name(self):
        return self.name
    def get_url(self):
        return self.url
    def get_description(self, classes):
        description = ""
        result = requests.get(self.get_url())
        search = BeautifulSoup(result.text, 'html.parser')
        text = search.get_text()
        index_1 = search.get_text().find("Credit Hours") + 13
        index_2 = 0
        if(search.get_text().find("Grading Restriction") != -1):
            index_2 = search.get_text().find("Grading Restriction")  
        if(search.get_text().find("Comment") != -1 and (search.get_text().find("Comment") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("Comment")
        if(search.get_text().find("(RE)") != -1 and (search.get_text().find("(RE)") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("(RE)")
        if(search.get_text().find("Recommended") != -1 and (search.get_text().find("Recommended") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("Recommended")
        if(search.get_text().find("Repeatability") != -1 and (search.get_text().find("Repeatability") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("Repeatability")
        if(search.get_text().find("(DE) Corequisite") != -1 and (search.get_text().find("(DE) Corequisite") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("(DE) Corequisite")
        if(search.get_text().find("(DE) Prerequisite") != -1 and (search.get_text().find("(DE) Prerequisite") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("(DE) Prerequisite")
        if(search.get_text().find("Registration Restriction") != -1 and (search.get_text().find("Registration Restriction") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("Registration Restriction")
        if(search.get_text().find("Satisfies") != -1 and (search.get_text().find("Satisfies") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("Satisfies")
        if(search.get_text().find("Contact Hour Distribution") != -1 and (search.get_text().find("Contact Hour Distribution") < index_2 or index_2 == 0)):
            index_2 = search.get_text().find("Contact Hour Distribution")
        if(search.get_text().find("(See") != -1):
            string = ""
            index_2 = search.get_text().find("(See") + 5
            for i in range(index_2, len(text)):
                if(text[i] == '.'):
                    break
                string += str(text[i])
            for item in classes:
                name = item.get_name()
                if(name.find(string) != -1):
                    return item.get_description(classes)
        if(index_2 == 0):
            index_2 = search.get_text().find("Back to Top")
        for i in range(index_1, index_2):
            description += str(text[i])
        return description

    def get_hours(self):
        result = requests.get(self.get_url())
        search = BeautifulSoup(result.text, 'html.parser')
        stuff2 = search.find_all('strong')
        for i in range(len(stuff2)):
            if(stuff2[i].text == "Credit Hours"):
                 return stuff2[i-1].text

def get_input(courses):
    inp = input('Enter a class: ')
    if(inp == EOFError or inp == 'quit'):
        return False
    for out in courses:
        string = out.get_name()
        if(string.find(inp) != -1):
            print("    Class:", out.get_name())
            print("    Credit Hours:", out.get_hours())
            print("    Description:", out.get_description(courses))
    return True

def main():
    urls = []
    names = []
    courses = []
    catalog_url = 'https://catalog.utk.edu/content.php?catoid=32&catoid=32&navoid=4393&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=1#acalog_template_course_filter'
    for j in range(1, 43):
        if(j > 1):
            change = "5D="
            change += str(j)
            initial = "5D="
            initial += str(j-1)
            catalog_url = catalog_url.replace(initial, change)
        result = requests.get(catalog_url)
        search = BeautifulSoup(result.text, 'html.parser')
        stuff = search.find_all('a')
        for tag in stuff:
            string = str(tag.get('href'))    
            if(string.startswith("preview")):
                urls.append(string)
        for tag in stuff:
            string = str(tag.get('title'))
            if(string.endswith("window")):
                index = string.find("opens")
                string_fin = ""
                for i in range(0, index):
                    string_fin += string[i]
                names.append(string_fin)
        for i in range(len(urls)):        
            Course = course()
            Course.add_name(names[i])
            class_url = "https://catalog.utk.edu/"
            class_url += urls[i]
            Course.add_url(class_url)
            courses.append(Course)
        urls.clear()
        names.clear()
    file1 = open("classes.txt", "w")
    for output in courses:
        name = output.get_name()
        url = output.get_url()
        file1.write(name)
        file1.write(url)
        file1.write('\n')
    file1.close()
    while(1):
        if(get_input(courses) == False):
            return
    
    
if __name__ == "__main__":
    main()