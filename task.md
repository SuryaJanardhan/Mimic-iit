-- single script repo mainly md files and analysis files including 
--py based automation for linkeding llm
-- funciton programmin only all funcs 
-- i have this script for automation of post creation of linkedin
-- mainitn g< 80% > of ratelimits of limits of linkedin porper so that acc cant be blocked 
-- core code snippet is curl -X POST "https://api.linkedin.com/rest/posts" \
  -H "Authorization: Bearer YOUR_FRESH_ACCESS_TOKEN" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Linkedin-Version: 202607" \
  -H "Content-Type: application/json" \
  --data '{
    "author": "urn:li:person:bT4mlIV3WS",
    "commentary": "Hello LinkedIn! This is my first test post using the official LinkedIn API ",
    "visibility": "PUBLIC",
    "distribution": {
      "feedDistribution": "MAIN_FEED",
      "targetEntities": [],
      "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": false
  }'

-- llm based post generation of linkedin
-- post creation must be based on the perivous posts and analysis of the posts
-- post must be engaging and following best practices for linkedin
-- post s mainnly depdens on the treending github repos 
-- trending tech ai concepts trending ai things trending tech things
-- if relevant img is ther attach it make it linkedin professional like not some ai slop 
-- no hastags must be attached to the posts at all 
-- for now my api has only basic access not every access i want to utilize those fully i can like or comment if i colud find some other people big guys vireal guys posts so that i can comment and like 
-- i want a func dedicated to the rate limits how many more calls left for todauy for this account any one error stops overall flow 
-- content mix: major content must be serious deep technical (GitHub trends, AI concepts, system design)
-- very little memes allowed (~10-15%): controlled mix of witty text-based memes and high quality image-based memes
-- strategic engagement models: value-add commenting on viral posts, 1st hour velocity optimization, zero outbound link post body
-- weekly email reporting: automated email dispatch summarizing post performance, account health, rate limit usage, and recommendations
-- content capability plan: 80% serious tech, 10% text memes, 5% image memes, 5% simulated text choice polls (since native API polls are restricted)
