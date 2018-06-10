## API remote tada!

Demos for the new API remote. It automatically opens up a server at localhost:8080 and listens to do your bidding.

Nothing like taking a deep dive into code you didn't write, in a language you don't know, that uses all sorts of magic AND threading to make you feel humble.

But, it works! Bulletproof and no crashes thus far.

#### usage

You can send direct_commands (usually to toggle something or set something specific) or value_commands, where you are sending a value in

#### examples

```
GET http://localhost:8080/?value_command=brightness&value=200

GET http://localhost:8080/?value_command=color&value=200&value_command=count&value=2&value_command=width&value=10

GET http://localhost:8080/?direct_command=slow

GET http://localhost:8080/?direct_command=noslow&value_command=brightness&value=50

```

note - you must send the value that goes with your value command right after you send the command.

#### open questions:
* Still can't figure out how to set values on the running animation if the animation is a sequence. Routing craps out on `animation.current_animation._value`

#### to do:
* Some sort of error handling response in API? Perhaps if no route matched...but not sure how we get back to that thread.

* Possibly get rid of the idea of direct_commands and value_commands entirely and let people specify in the yml file what params they want to use? Could just specify arbitrary params like ```
http://localhost:8080/?noslow=true&brightness=50
```
(that will be my first refactor)
