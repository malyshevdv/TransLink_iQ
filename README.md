2024-09-13
Have made DockerFile to run POS-emulator within docker container

docker build -t emulator .
docker run -d --name ashburn_pos_emulator -p 6678:6678 emulator

http://localhost:6678/
http://localhost:6678/docs

2024-09-03
I have completed POS-emulator. It provides you to develop your own solution without fizical ASHBURN TransLink API POS.
To start the emulator - run this command: fastapi dev --port 6678 deviceEmulator.py


2024-08-22
I have completed the library connection with all API-functions v107 in Python without business logic.

19-08-2024
I have completed the implementation of the synchronous and asynchronous methods of connecting to the software suite ASHBURN TransLink iQ ECR. This solution includes the implementation of the library connection with all API-functions v107 and the implementation of business logic: Authorize sales, Authorize void and Authorize partial void, close day operation, and print totals. 

![image](https://github.com/user-attachments/assets/8096d122-4f67-45f6-a84e-bd293fd421f8)

2024-08-08
I constantly have to work with cash and acquiring equipment, because the acceptance and accounting of money in trade is very important. Usually, to connect new equipment, a specific DLL library is used that is tied to this specific equipment model. When installing a new equipment model, you need to look for an updated library or change the accounting program.
 
ASHBURN International has implemented a universal approach to managing cash register equipment. ASHBURN International employees take on the setup of interaction with new equipment models. For integrators, two options for interacting with equipment are offered: ActiveX-connect and RestX-connect, which have a universal set of commands for external equipment.

Our universal solution, developed by ONESOFT, allows you to connect acquiring equipment that works through ASHBURN International TransLink.iQ software to your ERP, cash, and warehouse program. With our solution, we can make integration in a short time both with the accounting system of our production and with third-party programs.
We use the RestX-connect method for integration since it has no restrictions on the type of operating system used. 
Our solution is localized for English and Georgian. After integration, your system administrator can independently configure the new device in user mode as shown below.


