from codector.library import Codector


def test_returns_file_list_1(repo):
    codector = Codector(repo.working_dir)
    assert set(codector.files()) == {"file1.md", "file2.py", "file3.py", "file4.js"}


def test_returns_file_list_2(repo):
    codector = Codector(repo.working_dir)
    repo.add_file_change_commit(
        file_name="new_file.cpp",
        contents="#include <iostream>",
        author=repo.actors["John Doe"],
        commit_message="Initial commit for C++ file",
    )
    assert set(codector.files()) == {
        "file1.md",
        "file2.py",
        "file3.py",
        "file4.js",
        "new_file.cpp",
    }


def test_gets_files_from_all_branches(repo):
    codector = Codector(repo.working_dir)
    main = repo.active_branch
    new_branch = repo.create_head("other_branch")
    new_branch.checkout()
    repo.add_file_change_commit(
        file_name="file_on_other_branch.cpp",
        contents="",
        author=repo.actors["John Doe"],
        commit_message="add my file",
    )
    main.checkout()

    assert "file_on_other_branch.cpp" in codector.files()


def test_file_change_many_times_is_first_result(repo):
    codector = Codector(repo.working_dir)
    for i in range(10):
        repo.add_file_change_commit(
            file_name="new_file.txt",
            contents=f"{i}",
            author=repo.actors["John Doe"],
            commit_message="add my file",
        )

    assert codector.files()[0] == "new_file.txt"


def test_newer_change_can_beat_frequent_change_in_past(repo):
    codector = Codector(repo.working_dir)
    for i in range(10):
        repo.add_file_change_commit(
            file_name="old_file.txt",
            contents=f"{i}",
            author=repo.actors["John Doe"],
            commit_message="add my file",
        )
    repo.tick_fake_date(days=300)
    repo.add_file_change_commit(
        file_name="new_file.txt",
        contents="hello",
        author=repo.actors["John Doe"],
        commit_message="add another file",
    )

    assert codector.files()[0] == "new_file.txt"
