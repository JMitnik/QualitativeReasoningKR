gradient applying(GA)

(strictly after)

exo behaviour(EB) | relation propagation(RP).  

> mapped parallelly, since at least in our case, these two affect different vars. So we can deal with them separately and product together. Or, we can do one after another, the order is not important.

(strictly after)
extreme derivative clip(EDC)

for example:

```mermaid
graph TD
A -->|GA| B
A -->|GA| C
B -->|RP&EB| D
B -->|RP&EB| E

B -->|RP&EB| F
B -->|RP&EB| G

C -->|RP&EB| H
C -->|RP&EB| I
C -->|RP&EB| J

A[+0 ++ ++]
B[+0 m0 m0]
C[+0 ++ ++]

D[+- m0 m0]
E[+- m- m-]

F[+0 m0 m0]
G[+0 m- m-]

H[+0 +0 +0]
I[+- +0 +0]
J[+- ++ ++]
```

