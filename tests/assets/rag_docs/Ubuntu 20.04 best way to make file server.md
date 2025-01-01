# Ubuntu 20.04 best way to make file server?

Asked 3 years, 10 months ago
Modified 4 months ago
Viewed 23k times

5

I have recently read somewhere that you can simply host a file server with '''python3 -m http.server'''. I plan on using this on a PC running Ubuntu and access using my laptop so I don't have to have all my files on my laptop. Is this the best way to do it? I have seen many others using Apache, Samba and such. I just want to know which would be easiest to just access a few files.

server20.04files
Share
Improve this question
Follow
asked Feb 14, 2021 at 4:29
Deluminize's user avatar
Deluminize
8111 gold badge22 silver badges99 bronze badges
1
You can create a simple webserver using that command, but that's more along the lines of an example or proof-of-concept. It's insecure, and leaves your whole system wide open to anybody who happens by. It's a bad idea. For "just a few files" a free cloud storage service might be both convenient and secure. Running your own safe, secure file server connected to the dirty internet requires a bit more research on networking and security. – 
user535733
 CommentedFeb 14, 2021 at 4:44
@user535733 I want the files actually on my PC, not on the cloud. Is there any way to achieve that? – 
Deluminize
 CommentedFeb 14, 2021 at 4:53
What OS will you be using to remotely access the files? – 
user535733
 CommentedFeb 14, 2021 at 5:15
Also Ubuntu. And possibly windows but not nesscesary – 
Deluminize
 CommentedFeb 14, 2021 at 5:24
Are you willing to set up ssh keys for secure access? – 
user535733
 CommentedFeb 14, 2021 at 5:31
Show 2 more comments
3 Answers
Sorted by:

Highest score (default)
4

Install samba apt install samba samba-common-bin it is so simple to do too, edit one file, set password, restart daemon and your done. The nano /etc/samba/smb.conf in the [homes] section change the yes to no like below to have the share read/writable, at the bottom of the file add your share. Then set the password for the user_name you want to be able to access the share with smbpasswd -a user_name and restart samba service smbd restart. All commands run with sudo in front of them in the Terminal application.

 # By default, the home directories are exported read-only. Change the
 # next parameter to 'no' if you want to be able to write to them.
read only = no
snip ....
[share-name]
path = /home/user_name/share_directory
writeable=Yes
create mask=0777
directory mask=0777
public=no
You do not mention if this is local network only access, I would hope so securing server against the bots that scan the internet 24/7 is next to impossible for a normal user.

Share
Improve this answer
Follow
answered Feb 14, 2021 at 5:11
user1179897
Add a comment

4

Yes, python3 -m http.server is the most convenient way if you would like to download files remotely. No configurations needed.

However, it is definitely not for productive environment. There should be serious security and performance issue.

Share
Improve this answer
Follow
edited Aug 4, 2024 at 14:25
answered Feb 14, 2021 at 4:35
Limina102's user avatar
Limina102
29611 silver badge1111 bronze badges
1
Would there be any way to set a password or something? IDK the documentation confuses me – 
Deluminize
 CommentedFeb 14, 2021 at 4:37
@RelmRaydir In my memory not, there is very few configurable options. I use this at home to transfer files temporaily between my devices, but if it comes to long-term file transfer via public network, there should be better solutions. – 
Limina102
 CommentedFeb 14, 2021 at 5:33 
Add a comment
2

Here's one way.

Walk before you run. Start with exchanging files over ssh.

Look up how to set up ssh keys on your client and server for secure, passwordless login.

Pro Tip: NEVER trust password logins on the dirty, dirty internet. ALWAYS use keys.
Look up how to set up DDNS so you can locate your server from a remote location.

Now you are ready to upload and download files using the scp command. It's included with ssh, so nothing new to install.

Use 'sshfs' with your File Manager. Nautilus handles sshfs automatically -- it's part of the 'connect to server' feature. Windows plug-ins for sshfs are available.

Create a backup plan. Internet-connected servers get compromised. Hardware dies. Humans make typos that erase their data. If you data is worth all the effort to serve, then it's worth backing up regularly. Most trustworthy network backups are done over ssh.

Share
Improve this answer
Follow
answered Feb 14, 2021 at 5:58
user535733's user avatar
user535733
67.2k1212 gold badges118118 silver badges162162 bronze badges
I will tell you if this works later. PC broke down. – 
Deluminize
 CommentedFeb 14, 2021 at 9:46
For anybody stumbling upon this question, this is the solution. It should be the top answer. – 
Zi1mann
 CommentedNov 5, 2023 at 14:00 
Add a comment
You must log in to answer this question.
Not the answer you're looking for? Browse other questions tagged server20.04files.

## Ref
- https://askubuntu.com/questions/1316298/ubuntu-20-04-best-way-to-make-file-server
