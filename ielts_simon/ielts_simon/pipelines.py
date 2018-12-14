# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from ielts_simon.helper import Helper


class IeltsSimonPipeline(object):
    def process_item(self, item, spider):
        #if spider.name != 'ielts': return item
        file_name = 'data/%s/%s.%s.md' % (
            spider.name,
            Helper.trans_date(item['create_at'], spider.name),
            Helper.trans_url(item['entry_header'])
        )
        with open(file_name, 'w') as f:
            f.write('## %s\n' % item['entry_header'])
            f.write('\n> Author: %s' % Helper.get_author(spider.name))
            f.write('\n> Date: %s' % item['create_at'])
            f.write('\n> Category: %s' % item['category'])
            f.write('\n> Permalink: %s\n' % item['permalink'])
            content = ''
            for line in item['entry_content'].splitlines():
                line = line.strip()
                if len(line) > 0:
                    if line[0] == '_':
                        content += '\n'

                    if line[:2].isalpha():
                        content += '\n'

                    if '**' in line[:3]:
                        content += '\n'

                    content += '\n' + line

                    if '**' in line[-3:]:
                        content += '\n'

                    if line[-1] == ':':
                        content += '\n'

                    if 'Have my ebooks in your inbox in less than two minutes!' in line:
                        break

            f.write(content.replace('\n\n\n', '\n\n').replace('\n\n\n', '\n\n'))

