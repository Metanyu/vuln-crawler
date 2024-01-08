import json 
from pydriller import Repository

# repo = 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git'
# commit_code = 'fb18802a338b36f675a388fc03d2aa504a0d0899'

repo = 'https://github.com/curl/curl.git'
commit_code = 'fb4415d8aee6c1045be932a34fe6107c2f5ed147'


def get_full_commit():
    list_commit = [commit.hash for commit in Repository(repo).traverse_commits()]
    return list_commit


def see_what_in_single_pr():
    source_code = []
    for commit in Repository(repo, single=commit_code).traverse_commits():
        # print(commit.msg)
        for file in commit.modified_files:
#             print(file.source_code)
            source_code.append(file.source_code)
    return source_code

def main():
#     list_commit = get_full_commit()
    with open('/kaggle/input/snykkk/SNYK-RUST-DENO-1298032.json') as f:
        data = json.load(f)
    print(data)
    data['source_code'] = see_what_in_single_pr()
    # print(len(list_commit))
    # for i in list_commit:
    #     print(i)
#    print(data)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()