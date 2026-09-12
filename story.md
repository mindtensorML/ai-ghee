---
output: index.html
title: AI Ghee Making
description: I had this ghee every day growing up and never once made it. So I asked AI how, and then I asked it to do the whole thing for me.
og_title: The machine that knew when to stop
og_description: I had this ghee every day growing up and never once made it. So I built a machine that could feel the moment butter breaks.
og_image: images/ghee.jpg
og_url: https://mindtensorml.github.io/ai-ghee/
mark: AI Ghee Making
nav_text: The machine
nav_href: beast.html
nav_side: right
kicker: JD's AI GHEE
headline: The machine that knew when to stop
standfirst: I had this ghee everyday growing up and never once made it. So I asked AI how. Then I asked it to do the whole thing for me.
video: UG-S1qJc5ig
video_caption: The whole thing, in 60s
next_text: A closer look at the machine
next_href: beast.html
next_blurb: What it is made of, where the sensing happens, and what the rig actually watches.
footnote: The solid line is plotted from the sensor log of the run in these photographs, as a moving median with the middle half of the readings shaded behind it, because every raw sample drawn at once is a solid block of ink. The dashed line is the idealised shape of a churn, drawn by hand to show what the signal is looking for. The log and the script are in the repository.
---

## I had only ever eaten it

The ghee I know came from villages. Upcycled jars, from people who have made it the same way for so long that nobody there thinks of it as a technique.

It does not taste like the tin from the shop.

And I had never made a single batch. I did not know how long to leave the milk, or how cold the yogurt should be, or what the pot is supposed to sound like when it is ready.

## It starts with yogurt, not straight cream

Most industrial ghee begins with cream. The traditional way begins a day (or two) earlier, with cream (really boiled down whole milk) cultured into yogurt and left to sour overnight.

That souring is critical because you get clarified butter when you skip it. It is lovely, but it is not ghee.

![Yesterday's milk/cream, thickened overnight](images/yogurt.jpg "A wide steel bowl of thick set yogurt, held over a pot in a kitchen sink.")

## Two days on the counter

Warm milk, a spoonful of yesterday's yogurt stirred through, and then you leave it alone all night and let the bacteria get on with it. I let mine sit out for two days.

That is fermentation, and it is the step the commercial version skips. Live cultures, mostly Lactobacillus, work their way through the lactose and turn it into lactic acid. The milk thickens. It sours. By morning it is something else.

This is where everything good comes from. Lactose broken down so it sits easier. Fats and proteins made more bioavailable. Butyric acid, the short chain fatty acid your gut lining actually runs on, and more of it in ghee made this way than in ghee whipped up from sweet cream.

Ayurveda has prescribed this exact version for a very long time.

What I can tell you is that the culture is what makes the smell. That smell is most of the reason to bother with any of it.

![Set overnight, ready to churn](images/set-yogurt.jpg "A pot of thick set yogurt sitting in a kitchen sink, ready to be churned.")

## The method has a name

Bilona. Yogurt into a pot, a wooden churn dropped in, then you work it back and forth until the butter gives up and rises.

I made the churn myself. The ones I could find online were glued, and none of them would tell me what the glue was. That thing sits in your food for half an hour, so I was not going to guess. Hardwood, stainless steel screws, bolted onto a stirrer shaft I already had in a drawer.

Four arms and a steel band to hold them square. It is all screws, so it comes apart again.

![Screwed together, not glued](images/churn-front.jpg "The wooden churn head standing on a rail outdoors, four hardwood arms screwed to a steel shaft and held by a metal band.")
![Four arms, held square](images/churn-top.jpg "The churn head seen straight down its shaft, the four arms forming a cross with a stainless band clamped round the middle.")

It takes about half an hour and nothing interesting happens for most of it. Which makes it exactly the sort of job you daydream about handing to something else.

![The churn goes in. Nothing has happened yet.](images/bilona.jpg "A four armed wooden churn head resting in a pot of white yogurt.")

## So I asked

The people who actually know how to do this do not work from recipes, and none of them were in my kitchen. So the questions went into a chat window instead.

How long to culture. How cold to keep the yogurt. How fast you can spin it before friction warms the pot and ruins the butter. Every answer opened three more.

Then I asked the one I actually meant. Could you just do it?

> The question stopped being how do I make ghee. It became could you make it for me.

## The Beast

A cordless drill. The churn from a drawer and a hardware shop. A plastic food box for the electronics, a chopping board for a spine, and a large yellow stop button, because anything with a motor should have one.

It cost almost nothing and it looks like it. And that is sort of the point.

![The Beast](images/beast.jpg "The rig standing on a kitchen counter. A drill clamped to a wooden board, a clear plastic box of electronics, and a yellow emergency stop button.")

| Motor | Cordless drill, held in a clamp |
| Churn | Hardwood and stainless steel, made not bought |
| Brain | Raspberry Pi, logging once a second |
| Sense | Motor current for the churn, a temperature probe for the cook |
| Stop | One large button, wired to cut power |

## Spinning is the easy part

Anyone can spin yogurt. The hard part is knowing when to stop.

Stop early and you have thick froth. Go too long and you beat the butter back into the buttermilk and lose it. The window moves around depending on the fat, the temperature, and how the day is going.

Nobody times this. You listen for it. The sloshing goes from a smooth swirl to an uneven slap, and that is when you reach in.

![Twenty five minutes over the kitchen sink](images/churning.jpg "The drill running above a covered pot inside a stainless steel kitchen sink, with the electronics box alongside.")

## One sense, and only one

So I gave it one sense. It watches how hard the motor is pulling.

For twenty minutes, nothing. The load sits around 2700 mA and wanders about. Then the fat starts gathering and the drill has to push through something thicker. It climbs to 4700 and holds there for a moment, and then the butter lets go of the liquid and the load drops.

No camera, no model, nothing clever. A number that goes up and then drops.

![Motor current across the churn, from the log [*]](images/signal.svg "A chart of motor current across one churn. The load sits near 2700 milliamps for twenty minutes, climbs as the fat gathers, peaks near 4700, then falls away.")

## It stopped on its own

It ran. I went and did something else, and when I came back it had switched itself off.

Pale yellow curds sitting in cloudy buttermilk. Nobody told it the time. It worked that out from the only thing it could feel.

![The break](images/break.jpg "A pot of broken butter, pale yellow curds floating in cloudy buttermilk.")

## Then it is hands again

Gather the curds and press them into a ball. Rinse in cold water, over and over, until the water stops running cloudy.

Every drop of buttermilk you leave behind will burn in the next step. This part I did not automate, and I did not want to.

![Pressing it together](images/press.jpg "Two hands pressing loose butter curds together into a ball over a colander.")
![What is left behind](images/buttermilk.jpg "A pot of thin white buttermilk left in the sink after the butter has been lifted out.")

## The second sense

Motor load told the rig when to stop. The cook is a different problem, because now you are not looking for a moment, you are trying to hold one.

So the pot goes on a hotplate with a temperature probe in it, and an AC regulator that switches the plate on and off to keep the number where you put it. I set it to 250 F and it sat there for about an hour.

A person watching a pot for an hour will drift. The regulator does not get bored.

![Held at 250 for the whole cook](images/hotplate.jpg "The hotplate control panel with a red digital readout showing 250, and the rim of the ghee pot above it.")

## An hour of watching colour

Butter into the pot, and then it mostly just goes.

It melts. It foams white and loud. The water cooks off and the noise dies away. The milk solids sink and turn brown, and the smell shifts from butter to something toasted. When the pot goes quiet and the liquid runs clear, it is finished.

I watched most of it anyway, because it is a nice thing to watch. But nothing I did changed how it came out.

![Butter in](images/clar-1.jpg "A mound of pale washed butter sitting in a steel pot before any heat.")
![Foaming](images/clar-2.jpg "The pot full of loud white foam as the water boils out of the butter.")
![Clearing](images/clar-3.jpg "The liquid turning golden and translucent with small solids suspended in it.")
![Golden](images/clar-4.jpg "Deep golden fat bubbling with darkening milk solids across the surface.")
![Solids down](images/clar-5.jpg "Browned milk solids gathered at the bottom of the pot under a thin foam.")

## Ghee

Clear, amber, and it smells like the jars I grew up eating from. That was the only test I had, and it passed.

![Strained and still warm](images/ghee.jpg "A pot of finished ghee, deep clear amber with a little foam at one edge.")

It went into jars warm and clear. By the next day it had set pale and grainy.

I put a label on them. The word on it is Nepali for ghee, and the code beside it brings you back to this page.

![Two jars, set and labelled](images/jars.jpg "Two jars of pale set ghee on a wooden rail outdoors, each with a paper label carrying the Nepali word for ghee, the name JD's AI Ghee and a QR code.")

First batch I have ever made. I did not really make it.

## What I want next

Right now the machine knows two things. When to stop churning, and what temperature to hold.

Next I want to give it eyes and ears. A camera, so it can watch the foam break and the solids go brown and pick the heat itself instead of holding a number I handed it. And a microphone, because a lot of what tells you ghee is ready is the pot going quiet.

The drill could probably take a second shift too. Once the butter is in the pot it wants stirring, and there is already a motor sitting right there doing nothing.

Then the loop. Change the culture time, change the speed, taste what comes out, keep what worked, go again. Thirty runs and it would land somewhere I would not have thought to look.

I never really knew where to look anyway.
