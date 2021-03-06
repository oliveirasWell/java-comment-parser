# -*- coding: utf-8 -*-

import os

from commentParser.JavaParser import JavaParser as Parser
from commentParser.utils.linguage_definitions import java as linguage

NUMERO_DE_TAGS_A_PARSEAR = 2

repo_list = [repo for repo in linguage['repos']]

root_output_dirs = 'temp'

git_tag_command = 'git tag'
git_fetch_all_tags = 'git fetch --all --tags --prune'
git_checkout_tag_command = 'git checkout tags/%s -b %s'

is_to_create_clone_repos = True

def is_string_list_in_file(file_extension_list, file):
    for file_extension in file_extension_list:
        if file_extension in file:
            return True
    return False


def recursive_parser(directory_in):
    os.chdir(directory_in)

    for file in os.listdir('.'):
        # auto verify the type of the file, then parse it with the correct parser
        if is_string_list_in_file(linguage['file_extensions'], file):
            print(file)

            print('/---file---')
            parser = Parser(file, False)
            print(parser.parse())
            del parser
            print('----file---/')

    children = next(os.walk('.'))[1]

    print('/----children-----')
    print(children)
    print('----children-----/')

    for child in children:
        recursive_parser(child)

    os.chdir("..")


if __name__ == '__main__':

    for repo in repo_list:

        # Clona se não existir a pasta
        if is_to_create_clone_repos and not repo[1] in os.listdir('.'):
            print("clonando repo: %s", repo[0])
            os.system('git clone ' + repo[0])

        # entra na pasta
        os.chdir(repo[1])

        # fetch em todas as tags
        list_of_tags = os.popen(git_tag_command).read()
        list_of_tags = [i for i in list_of_tags.split('\n') if i]
        tam = int(len(list_of_tags) / NUMERO_DE_TAGS_A_PARSEAR)
        list_of_10_best_tags = [list_of_tags[i * tam] for i in range(NUMERO_DE_TAGS_A_PARSEAR)]

        # atualiza o estado do git
        os.system(git_fetch_all_tags)

        # parseia para cada arquivo
        for tag in [x for x in list_of_10_best_tags]:
            print('/--------tag-----------')
            print(tag)
            print('---------tag----------/')

            print(git_checkout_tag_command % (tag, '__aux' + tag))

            os.system(git_checkout_tag_command % (tag, '__aux' + tag))

            actual_directory = next(os.walk('.'))[1]
            for directory in actual_directory:
                print("------------------------------------------------------")
                print("Folder: " + directory)
                recursive_parser(directory)
                print("-----")

        os.chdir('..')
        print("----- Ended repo -----")
