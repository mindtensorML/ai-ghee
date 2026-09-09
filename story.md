---
output: index.html
title: AI Ghee Making
description: I had eaten village ghee all my life and never once made it. So I asked AI how, and then I asked it to do the whole thing for me.
og_title: The machine that knew when to stop
og_description: I had eaten village ghee all my life and never once made it. So I built a machine that could feel the moment butter breaks.
og_image: images/ghee.jpg
og_url: https://mindtensorml.github.io/ai-ghee/
mark: AI Ghee Making
nav_text: The machine
nav_href: beast.html
nav_side: right
kicker: Jay's AI GHEE
headline: The machine that knew when to stop
standfirst: I had this ghee everyday growing up and never once made it. So I asked AI how. Then I asked it to do the whole thing for me.
video: dEwIoD-T4lI
video_caption: The whole thing, start to finish V1
next_text: A closer look at the machine
next_href: beast.html
next_blurb: What it is made of, where the sensing happens, and what the rig actually watches.
footnote: * The chart on this page is based on real data but stylised for clarity. It was plotted from a raw sensor log.
credit: Photographs are from a single run, August 2026.
---

## I had only ever eaten it

The ghee I know came from villages. Upcycled jars, from people who have made it the same way for so long that nobody there thinks of it as a technique.

It does not taste like the tin from the shop. It is not close.

And I had never made a single batch. I did not know how long to leave the milk, or how cold the yogurt should be, or what the pot is supposed to sound like when it is ready.

## It starts with yogurt, not straight cream

Most industrial ghee begins with cream. The traditional way begins a day (or two) earlier, with cream (really boiled down whole milk) cultured into yogurt and left to sour overnight.

That souring is critical because you get clarified butter when you skip it. It is lovely, but it is not ghee.

![Yesterday's milk/cream, thickened overnight](images/yogurt.jpg "A wide steel bowl of thick set yogurt, held over a pot in a kitchen sink.")

## Next Steps

Warm milk, a spoonful of yesterday's yogurt stirred through, and then you leave it alone all night and let the bacteria get on with it. I let mine sit out for two days.

That is fermentation, and it is the step the commercial version skips. Live cultures, mostly Lactobacillus, work their way through the lactose and turn it into lactic acid. The milk thickens. It sours. By morning it is something else.

This is where everything good comes from. Lactose broken down so it sits easier. Fats and proteins made more bioavailable. Butyric acid, the short chain fatty acid your gut lining actually runs on, and more of it in ghee made this way than in ghee whipped up from sweet cream. 

Ayurveda has prescribed this exact version for a very long time,..

I can tell you is that the culture is what makes the smell, and the smell is not a small thing. It is most of what you are actually after.

![Set overnight, ready to churn](images/set-yogurt.jpg "A pot of thick set yogurt sitting in a kitchen sink, ready to be churned.")

## The method has a name

Bilona. Yogurt into a pot, a wooden churn dropped in, then you work it back and forth until the butter gives up and rises.

I made the churn myself. The ones I could find online were glued, and none of them would tell me what the glue was. That thing sits in your food for half an hour, so I was not going to guess. Hardwood, stainless steel screws, bolted onto a stirrer shaft I already had in a drawer.

It takes about half an hour and nothing interesting happens for most of it. Which makes it exactly the sort of job you daydream about handing to something else.

![The churn goes in. Nothing has happened yet.](images/bilona.jpg "A four armed wooden churn head resting in a pot of white yogurt.")

## So I asked

The people who actually know how to do this do not work from recipes, and none of them were in my kitchen. So the questions went into a chat window instead.

How long to culture. How cold to keep the yogurt. How fast you can spin it before friction warms the pot and ruins the butter. Every answer opened three more, and underneath all of them sat one I kept not asking.

Then I asked it. Could you just do it?

> The question stopped being how do I make ghee. It became could you make it for me.

## The Beast

A cordless drill. The churn from a drawer and a hardware shop. A plastic food box for the electronics, a chopping board for a spine, and a large yellow stop button, because anything with a motor should have one.

It cost almost nothing and it looks like it. And that is sort of the point.

![The Beast](images/beast.jpg "The rig standing on a kitchen counter. A drill clamped to a wooden board, a clear plastic box of electronics, and a yellow emergency stop button.")

| Motor | Cordless drill, held in a clamp |
| Churn | Hardwood and stainless steel, made not bought |
| Brain | Raspberry Pi, logging once a second |
| Sense | Motor current and voltage, nothing else |
| Stop | One large button, wired to cut power |

## Spinning is the easy part

Anyone can spin yogurt. The difficult part is knowing when to stop.

Stop early and you have thick froth. Go too long and you beat the butter back into the buttermilk and lose it. There is a window, and it moves with the fat content, the temperature, and the day.

Nobody times this. You listen. The sloshing changes from a smooth swirl to an uneven slap, and that is your cue to reach in.

![Twenty five minutes over the kitchen sink](images/churning.jpg "The drill running above a covered pot inside a stainless steel kitchen sink, with a red battery pack alongside.")

## One sense, and only one

So I gave it one sense. It watches how hard the motor is pulling.

For the first quarter of an hour, nothing. Then the fat starts gathering and the drill has to push through something thicker. The current climbs, and it keeps climbing, right up until the butter lets go of the liquid. Then the load falls off a cliff.

That fall is the whole idea. No camera. No model. A number that goes up, and then drops.

![Motor current across one churn [*]](images/signal.svg "A chart of motor current across one churn. The line sits flat for roughly fifteen minutes, climbs as the fat gathers, peaks, then falls away sharply where the machine stops.")

## It stopped on its own

It ran. I went and did something else. When I came back it had switched itself off.

Pale yellow curds sitting in cloudy buttermilk. Nobody told it the time. It worked out the moment from the only thing it could feel.

![The break](images/break.jpg "A pot of broken butter, pale yellow curds floating in cloudy buttermilk.")

## Then it is hands again

Gather the curds and press them into a ball. Rinse in cold water, over and over, until the water stops running cloudy.

Every drop of buttermilk you leave behind will burn in the next step. This part cannot be automated, and honestly I did not want it to be.

![Pressing it together](images/press.jpg "Two hands pressing loose butter curds together into a ball over a colander.")
![What is left behind](images/buttermilk.jpg "A pot of thin white buttermilk left in the sink after the butter has been lifted out.")

## An hour of watching colour

Butter into a pot, low heat, and then you wait.

It melts. It foams white and loud. The water cooks off and the noise dies away. The milk solids sink and turn brown, and the smell shifts from butter to something toasted. When the pot goes quiet and the liquid runs clear, it is finished.

![Butter in](images/clar-1.jpg "A mound of pale washed butter sitting in a steel pot before any heat.")
![Foaming](images/clar-2.jpg "The pot full of loud white foam as the water boils out of the butter.")
![Clearing](images/clar-3.jpg "The liquid turning golden and translucent with small solids suspended in it.")
![Golden](images/clar-4.jpg "Deep golden fat bubbling with darkening milk solids across the surface.")
![Solids down](images/clar-5.jpg "Browned milk solids gathered at the bottom of the pot under a thin foam.")

## Ghee

Clear, amber, and it smells like the jars I grew up eating from. That was the only test I had, and it passed.

First batch I have ever made. I did not really make it.

![Strained and still warm](images/ghee.jpg "A pot of finished ghee, deep clear amber with a little foam at one edge.")

## What I want next

Right now the machine knows exactly one thing. Stop here.

Next I want it to run the whole loop on its own. Change the culture time. Change the speed. Taste what comes out, keep what worked, throw away what did not, and go again. Do that thirty times and it will land somewhere I would not have thought to look.

Which is fine by me. I never knew where to look in the first place.

That is the actual experiment. The ghee is just what came out of the pot.
