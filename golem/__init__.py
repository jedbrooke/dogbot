#!/usr/bin/env python3
import asyncio
import datetime
import json
import os
import shlex
import sys
import uuid
from typing import AsyncIterable

import apprise
from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm

apobj = apprise.Apprise()
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"env.json")
env = json.load(open(env_path))
apobj.add(env["webhook"])


output_file = os.path.join(os.path.dirname(__file__),"output",f"image-{uuid.uuid1()}.png")

async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script = context.new_script(timeout=datetime.timedelta(hours=1))

        apobj.notify(body="starting job", title=f"task: {task.data} is starting")
        future_result = script.run(*shlex.split(f"/usr/local/bin/python3 /txt2img.py {shlex.quote(task.data)} '/golem/output/output.png' --offline"))

        script.download_file("/golem/output/output.png", output_file)

        yield script

        task.accept_result(result=await future_result)
        apobj.notify(body="finished job", title=f"task: {task.data} is finished")


async def main(prompt: str):
    package = await vm.repo(
        image_hash="bf0bfedb65309eccab85ee6e93517d0bf66f7d00057a52cb45c299ef",
        image_url="http://auto-editor.online/images/dog.gvmi",
        min_mem_gib=6,
        min_storage_gib=8,
        min_cpu_threads=4
    )

    tasks = [Task(data=prompt)]

    async with Golem(budget=10.0, subnet_tag="public") as golem:
        async for completed in golem.execute_tasks(worker, tasks, payload=package, max_workers=len(tasks), timeout=datetime.timedelta(hours=1)):
            print(completed.result.stdout)

def generate_image(prompt: str):
    
    enable_default_logger(log_file=os.path.join(os.path.dirname(__file__),"logs",f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log"))

    loop = asyncio.get_event_loop()
    task = loop.create_task(main(prompt))
    loop.run_until_complete(task)
    return output_file

if __name__ == "__main__":
    print(generate_image(" ".join(sys.argv[1:])))