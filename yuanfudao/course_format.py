import json

if __name__ == '__main__':

    head = '\t'.join(["课程名称", "课程时间", "课程目标", "课程价格", "课程配额", "课程链接", "教师名称", "教师链接"])

    with open('course_details.json', 'r') as fp:
        course_details = json.load(fp)

    context = [head]
    for course_detail in course_details:
        line = '\t'.join([
            course_detail['course_name'],
            course_detail['course_time'],
            course_detail['course_fit'],
            course_detail['course_price'],
            course_detail['course_quota'] if course_detail['course_quota'] != "" else "已报满或无信息",
            course_detail['course_url'],
            course_detail['teacher_name'],
            course_detail['teacher_url'],
        ])
        context.append(line)

    context = '\n'.join(context)

    with open('course_details.csv', 'w') as fp:
        fp.write(context)

