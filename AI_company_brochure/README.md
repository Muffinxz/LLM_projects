
### Requirements:

you will find the packages needed for this project in requirements.txt


### BUSINESS CHALLENGE:

Create a product that builds a Brochure for a company to be used for prospective clients, investors and potential recruits.

We will be provided a company name and their primary website.

See the end of this notebook for examples of real-world business applications.

And remember: I'm always available if you have problems or ideas! Please do reach out.

## First step: Have GPT-5-nano figure out which links are relevant

### Use a call to gpt-5-nano to read the links on a webpage, and respond in structured JSON.  
It should decide which links are relevant, and replace relative links such as "/about" with "https://company.com/about".  
We will use "one shot prompting" in which we provide an example of how it should respond in the prompt.

This is an excellent use case for an LLM, because it requires nuanced understanding. Imagine trying to code this without LLMs by parsing and analyzing the webpage - it would be very hard!


## Second step: make the brochure!

Assemble all the details into another prompt to GPT-5-nano

### Stream the answers:
With a small adjustment, we can change this so that the results stream back from OpenAI,
with the familiar typewriter animation