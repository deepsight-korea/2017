# Git tutorial

- 생활코딩에서 지옥에서 온 Git 강의 내용을 정리하였다.

***
## 자주 사용하는 명령어 정리

1. (master) **git branch** *branch1* <br>
: 자료 작성을 위한 *branch1* 를 생성한다.

2. (master) git checkout *branch1* <br>
: branch1로 이동한다.

2. (branch1) **git add** *filename*  <br>
: 파일 수정 후 해당 변경 사항을 add해준다.

3. (branch1) **git commit -m** "변경 사항" <br>
: 파일 수정 후 해당 변경 사항을 commit해준다.  

4. (branch1) **git pull --rebase origin** [master] <br>
: 온라인 저장소의 master 내용과 동기화시킬 때 사용한다. 수정 내용을 push하기 전에 항상 먼저 사용해야 한다.
  - conflict가 발생할 경우 git rebase --abort를 입력하면 pull 이전 상태로 돌아간다.
  - conflict를 해결하고 push하고 싶은 경우엔 git add *충돌 파일명*, git rebase --continue를 입력해주자.
  이 때, master는 continue된 commit 뒤에 존재하게 된다. (master는 따로 merge해줘야 함.)

5. (github사이트) **New pull requests**  <br>
: pull requests 창을 열어서 merge하려는 변경 사항에 대한 논의, 피드백, 수정을 진행한다.
그리고 해당 수정 완료 후 해당 창에서 merge를 수행한 후에 로컬에 master를 pull한다.

6. (master) **git merge** *branch1* <br>
: master와 branch1을 합친다.

7. (master) **git push -u origin** [master] <br>
: 로컬 저장소의 내용을 온라인 저장소의 master에 업로드한다.

***
## 수업 내용
**Git Bash** : Windows에서 Linux 기반의 명령어를 사용할 수 있도록 해주는 프로그램이다.
  - ls -al : 현재 작업 폴더 내 파일 정보 확인 명령어
  - clear : 지난 입력/출력 내용을 다 지운다.
  - vim 1.txt : 1.txt를 생성한다. i를 누르면 입력 가능.
  - cat 1.txt : 1.txt 내용 확인.


## Git 명령어

1. **git init** : 현재 작업 폴더를 git 작업 폴더로 만들어주면서 .git 폴더를 생성하며 해당 폴더에 버전
관련 정보가 누적되게 된다.
  - *name* : name 이름의 git을 생성한다.
  - --bare *name* : **저장소** 로 git을 생성한다. (기타 작업 불가능)

2. **git status** : 현재 상태 확인

3. **git add** *filename* : git에 관리하는 파일 추가/수정 사항 추가

4. **git config --global user.name** *username* : 작업 시에 누가 했는지 알려줌

5. **git config --global user.email** *useremail* : 작업 시에 어떤 이메일이 했는지 알려줌

6. **git commit** : 버전을 업데이트한다.
  - -a : add를 자동으로 한다.
  - -m : message를 editor를 안 키고 업데이트하겠다.
  - -am : 위 2개를 합친 내용
  - --amend : commit 내용을 바꾼다. 원격저장소 내용을 바꾸기 전(**push**)에 하는 명령어이다.

7. **git log** : 버전 업데이트 상황 확인한다.
  - -p : 이전 commit과의 변경점을 보여준다.
  - *commit id* : loginfo에 해당되는 commit의 변경점을 보여준다.
  - --branches --decorate --graph (--oneline) : branch 간의 변동 사항을 보여준다.
  - (-p) *branch1*..*branch2* : branch1에는 없고 branch2에는 있는 것들을 보여준다. (-p 유무에 따라 내용 출력)
  - --reverse : 순서를 거꾸로 본다. (처음/끝 반대)

8. **git diff** : 현재 작업에 대한 변경점을 보여준다. (commit 전, add시 사라짐)
  - *commit id1*..*commit id2* : log1과 log2의 commit을 비교해서 나타내준다.  

9. **git reset** :
  - *loginfo* --hard : loginfo이 후의 버전을 삭제하고 해당 loginfo단계로 돌아간다.
  - --hard : 현재 add, commit 등 상태를 다 없애버린다.(***자주 사용***)

10. **git revert** : 스킵

11. **git 명령어 --help** : 명령어에 해당되는 도움말 확인

12. **git branch** : branch를 확인한다.
  - *branch1* : 새로운 branch1을 생성한다. 생성 당시 이전 상태와 완전 동일하다.
  - -d *branch1* : branch1을 삭제한다.

13. **git checkout** *branch1* : 작업 branch를 branch1로 변경한다.
  - -b *branch1* : branch1을 만들고 checkout한다.
  - *commit id* : commit id에 해당되는 상태를 보여준다.

14. **git merge** : merge할 때는 추가되는 내용을 받으려는 branch로 checkout되어 있어야 한다. merge했을 때 2개의 부모를 갖는 commit이 된다.
  - *branch1* : branch1의 내용을 병합한다. 다른 부분이 수정되면 자동으로 합쳐진다.
  겹칠 경우에 ***======*** 를 기준으로 위, 아래 내용을 수정해야 한다.

15. **git stash** : 다른 branch에서 작업하던 내용을 숨겨놓을 수 있다. 기본적으로 branch에서 수정한 내용을 commit하지 않고 checkout하면
master에까지 영향을 미친다. stash를 하면 해당 branch에 저장된다. git status하면 이전 상태로 보여진다. <br>
git stash로 저장한 내용은 reset을 해도 사라지지 않는다 drop을 해주어야 사라진다. (*다시 apply로 불러올 수 있음.*)
untracked file에 대해서는 stash가 불가능하다. (새로 생성된 파일)
  - apply : 숨겨놓았던 내용을 불러온다. (최근꺼부터 순차적으로)
  - list : list를 보여준다.
  - drop : 가장 최신 stash를 삭제한다.
  - pop : apply + drop

16. **git remote**
  - add origin *repository* : push할 저장소를 지정해주고 origin으로 칭한다. origin은 로컬 저장소와 연결되어 있는 기본
  적인 저장소라고 생각하면 되며 다른 이름의 저장소도 있을 수 있다.(e.g. friend) 그럼 해당 저장소로 로컬 내용을 올릴 수도 있다.
  - -v : fetch, push 연결 사항 확인해준다.  
  - remove *origin* : remote하는 origin을 지운다.

17. **git push**
  - (-u) origin [master] : master로 commit 내용을 push해준다. -u는 최초에 local과 원격저장소를 연결해줄 때 사용한다. 이 후에 사용 필요 없음.

18. **git clone**
  - *url* *repo1* : url 내용을 repo1에 clone한다.

19. **git pull origin [master]** : 원격저장소의 내용을 로컬로 가져온다.


git commit 전에는 항상 git add가 와야한다. 파일 하나 하나에 대해서 선택적으로 변경사항에 대해
commit해야 할 필요성이 있기 때문이다. (기존 버전 관리 시스템과 차별화된 점이라고 한다.)

commit 대기 상태는 ***stage area*** 에 있는 것이다.
git에는 stage(*commit 대기*)와 repository(*commit 완료값*)라는 개념이 존재한다.

commit 마다 주소가 존재한다. 이를 통해서 log를 알 수도 있다.

reset과 revert의 차이점을 알아야 한다.
reset을 하면 log가 사라지긴 하는데 다시 복구할 수도 있다.
reset은 협업 시에 절대 사용하면 안 된다.

git merge에서 fast-forward는 빨리감기이다.
master를 기반으로 branch1를 만들었을 때 branch1을 commit하고 master를 어떤 변경도 하지 않은 상황에서 branch1 내용으로 merge하면 그냥 branch1로 이동하는 것이다. (commit을 생성하지 않는다.)
master도 바꾸고 branch도 바꾸면 recursive를 하게 된다.
공통의 조상을 찾고 둘을 합치고 별도의 commit을 만든다.

***
## Git의 원리

1. **git add**
  - 폴더 내 변경 점은 add 전에는 git에 아무런 영향을 주지 않는다.
  - 변경점을 add할 시에 object폴더 내 파일을 바라보게 하는 index가 생성되고 파일의 값은 object에 저장된다.
  index의 두 글자가 object내 폴더명, 나머지가 파일명이 된다.
  - 같은 파일의 값들은 하나의 object에 저장되게 되어 같은 내용의 파일은 모두 같은 index를 갖게 된다.
  (중복에 대한 비효율을 막기 위함.)
  - 상세한 원리는 sha1라는 알고리즘(?)을 통해서 hash값을 얻는 방법이라고 한다. <br>
  *※ 의문점 : 같은 파일에 대한 index를 준다고 해도, 서로 중복되는 파일이 왠만하면 없을텐데? 흠..*

2. **git commit**
  - commit시에 object폴더 내 파일이 생성되고 파일 내에 작성자, comitter 정보 외에 tree라는
  정보가 추가적으로 들어가고 link가 걸리는데, 그 안에는 업데이트할 당시의 파일의 이름과 내용이 있다.
  (현재 상태를 사진찍는 것) 또한, 추가적으로 parent에 해당되는 commit의 정보도 줘서 이전 commit으로
  연결될 수 있게 한다.
  - object 파일의 구성
    - blob : 파일의 내용을 가짐 (코드)
    - tree : 파일명, blob의 정보를 가짐 (해당 상태의 blob 모임)
    - commit : commit에 대한 정보를 가짐 (commit 내용, 작성자, tree, parent)

3. **git status**
  - 현재 index값과 현재 파일의 hash값을 비교했을 때 다르면 add할게 있다는 뜻이다. (**Changes not staged
  for commit**)
  - add하면 index와 object가 생성된다. index와 현재 파일의 hash값이 같다. (**Changes to be commited**)
  - 최신 commit의 tree와 현재 index를 비교해서 같지 않으면 commit할게 있다는 뜻이다. <br>
  ***파일 - index, tree - index 두 조건 비교를 통해서 현재 상황을 파악하는 거네***

4. **git branch**
  - git을 처음 만들면 HEAD라는 파일 생성. refs/heads/master를 링크로 가리킨다. master는 가장 ***최신*** 커밋을 가리킨다.
  git log를 했을 때 최신 커밋을 알 수 있는 이유는 head -> master -> 최신 커밋을 가리키는 구조로 되어있기 때문이다.
  이전 커밋은 parent를 통해서 탐색하면 된다.
  - git branch exp를 하면 refs/heads/exp가 생성된다. exp/master로 checkout하면 HEAD파일이 exp/master를 가리킨다.
  - 전부다 tree형태로 이어져있고 각각의 branch, commit, 내용 등 모든 것들이 단순한 파일(텍스트?)형태로 이루어져 있다.
  - git을 하다보면 보이는 (HEAD -> master)는 지금 checkout되어 있는 branch를 나타낸다.

5. 원격저장소
  - Fork : 누르면 해당 소스코드가 나의 것이되며 이를 마음대로 수정할 수 있다. 개발자들은 자신들의 프로젝트를
  개방하고 가져가서 다른 사람들이 활용하길 바라는 측면이 있다.
  - ssh(secureshell) : https와 다른 통신 방식의 일종이다. https와는 달리 자동 로그인을 제공한다는 장점이 있다. ssh는
  각자 컴퓨터에서 생성 가능하며 이는 id_rsa, id_rsa.pub이라는 두 개의 파일로 저장이 된다. 자세한 내용은 생략하지만
  두 개의 상호작용으로 로그인을 생략해준다고 한다.
    - id_rsa : private key 내 노트북에 저장된다.
    - id_rsa.pub : public key 서버 컴퓨터에 저장된다.

git 내에서 이루어지는 활동을 도식화해놓은 그림은 아래와 같다. <br><br>
![Git Data Transport Commands](https://onezeronull.com/files/2016/06/Git-data-transport-commands.png)

Reference: <br>
[생활코딩 - 지옥에서 온 Git](https://opentutorials.org/course/2708) <br>
[아틀라시안 - Git 협업 flow 설명](https://www.atlassian.com/git/tutorials/comparing-workflows) <br>
Git 데이터 흐름 이미지 : https://onezeronull.com/2015/04/10/git-diagram-for-data-transport-commands/ <br>
