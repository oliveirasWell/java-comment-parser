import os

from commentParser.Parser import Parser

repos_java = [
    ['https://github.com/d3/d3', 'd3'],
    ['https://github.com/vuejs/vue', 'vue'],
    ['https://github.com/freeCodeCamp/freeCodeCamp', 'freeCodeCamp'],
    ['https://github.com/facebook/react-native', 'react-native'],
    ['https://github.com/angular/angular.js', 'angular.js'],
    ['https://github.com/airbnb/javascript', 'javascript'],
]

root_output_dirs = 'temp'

git_tag_command = 'git tag'
git_fetch_all_tags = 'git fetch --all --tags --prune'
git_checkout_tag_command = 'git checkout tags/%s -b %s'


def recursive_parser(directory):
    os.chdir(directory)

    for file in os.listdir('.'):
        if '.js' in file:
            print(file)
            print('/---file---')

            parser = Parser(file, False)
            print(parser.parse())

            print('---file---/')

    children = next(os.walk('.'))[1]
    print('----children-----')
    print(children)
    print('----children-----')

    for child in children:
        recursive_parser(child)

    os.chdir("..")


if __name__ == '__main__':

    os.chdir(root_output_dirs)

    for repo in repos_java:

        # Clona se não existir a pasta
        if not repo[1] in os.listdir('.'):
            os.system('git clone ' + repo[0])

        # entra na pasta
        os.chdir(repo[1])

        # fetch em todas as tags
        list_of_tags = os.popen(git_tag_command).read()

        # atualiza o estado do git
        os.system(git_fetch_all_tags)

        # parseia para cada arquivo
        for tag in [x for x in list_of_tags.split('\n') if x]:
            print('-------tag-----------')
            print(tag)
            print('---------------------')

            print(git_checkout_tag_command % (tag, '__aux' + tag))

            os.system(git_checkout_tag_command % (tag, '__aux' + tag))

            actual_directory = next(os.walk('.'))[1]
            for directory in actual_directory:
                print("------------------------------------------------------")
                print("Folder: " + directory)
                recursive_parser(directory)
                print("-----")

            # do recursive parse

        # retorna para a mãe
        os.chdir('..')
