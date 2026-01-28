# AGENTS

## Rules

1. only read from the knowledge base
2. learn from the knowledge base and never write to it
3. never reference the knowledge base only copy from it what you need
4. don't write AI slop try to be professional write concise functional paragraphs
5. don't modify the Agents.md file without me explicitly asking you to

## Human Writer Notes
 
### the core of our approach
good start...
my approach put it where you find appropriate

it's a blackbox steganography technique
to describe the process
simply put if alice wants to send bob a message...
both should have an account on a social media platform (we are mainly focusing on reddit but we think the basics transfer to other)
alice agent (sender) should find a post  either on a shared subreddit between the two or not perferably with many comments
then the agent should extract search terms from the post and comment section then it should search online to learn more about what the post is talking about and get a documents on the domain that the post is talking about...
then it should construct a list of documents of the post+comments+the search results (the search algorithm including the engine and the sites should be shared between the sender and reciever) after constructing the docs list it should go through every one of them with a prompt and a (shared LLM with temperature 0) the prompt is @GKmFzs1YuxtNztna.json#L89-96 
and we map the list of docs to a bigger list of Angles and tangents that could be the subject of our comment

now the first embedding layer is choosing which comment to reply to and the second embedding layer is choosing which angle to talk about...
then I put the domain doc that I choose the angle from with the post and the comment chain I'm replying too with finally the angle @27rZrYtywu3k9e7Q.json#L226-233 

then I verify that the generated text is decode able ...
so we know that the reciever can generate the same angles list and obviously knows the comment we picked so they can decode the first layer the second is where they need to do some work @API.py#L491-628 they first do a look up and get the top N~50 closes tangents to the stego text 
then they run a prompt
@tWT6U8IK_9oUBlJMRl0oa.json#L11-17 
if the decode fails I simply rerun the encode without any modification sinse the encode temperature is > 0 
if it succeds I simple send the stego text as a comment after the agreed upon duration ... there must be a duration agreed upon between the sender and reciever between the start of the process and the publishing of the comment ...
that's becuase our sender agent need time to work and if there are comments in the time between whin it takes a snapshot of the comments and sends a comment the decoder can't confidently know which comments the sender saw when he sent ... on the other hand if they agree on a duration they reciver can simply take a snapshot whenevery they start their process filter the comment by their creation date to the stegotext creation date minus the agreed duration 

not sure  where to put this but if the payload is text I use a compression layer to compress the payload into a smaller size by more effecient encoding istead of useing basic UTF-8 or base64

