#!/usr/bin/env python3

import facebook
import json

TOKEN='ASDASDFASDASDASFD'
PAGE_ID='11111111111111'
QUERY = facebook.GraphAPI(access_token=TOKEN,version="3.1")

def published_post():

    posts = QUERY.get_object(id=PAGE_ID, fields='published_posts')
    posts_ids = []
    data = {}

    print("Extract id posts")
    for post in posts['published_posts']['data']:
        posts_ids.append(post['id'])
        data.update({post['id']:'message': post['message'],'created_time': post['created_time']})
#        print("ID: ", post['id'])
    
    if posts['published_posts']['paging']['cursors']['after']:
        key_after = posts['published_posts']['paging']['cursors']['after']
        after = QUERY.request(PAGE_ID+'/published_posts?limit=25&after='+key_after)
        try:
            while (bool(after['paging']['cursors']['after'])):
                try:
                    for more_posts in after['data']:
                        posts_ids.append(more_posts['id'])
                        data.update({more_posts['id']:{'message':more_posts['message'], 'created_time':more_posts['created_time']}})
#                        print("ID__: ", more_posts['id'])
                        after = QUERY.request(PAGE_ID+'/published_posts?limit=25&after='+after['paging']['cursors']['after'])
                except Exception as e:
#                   print("Error in paging posts: ", e)
                    pass
        except Exception as e:
#            print("Error in: ", e)
            pass

    with open('posts_data.json', 'w') as write_file:
        json.dump(data, write_file)
    return posts_ids


def reactions(ids):
    data = {}
    print ("Extract reactions to posts")
    for id_p in ids:
        react_post = QUERY.get_object(id=id_p, fields='reactions.summary(total_count)')
        data.update({id_p:{}})
#        print("id_p: %r and summary: %r" % (id_p,react_post['reactions']['summary']['total_count']))
        data[id_p].update({'summary':react_post['reactions']['summary']['total_count']})
        for react in react_post['reactions']['data']:
            data[id_p].update({react['id']:{'name':react['name'],'type':react['type']}})
#            print("Post ID: %s  name: %s  reaction: %s" % (id_p,react['name'],react['type']))
            if react_post['reactions']['paging']['cursors']['after']:
                key_after = react_post['reactions']['paging']['cursors']['after']
                after = QUERY.request(id_p+'/reactions?limit=25&after='+key_after)
                if bool(after['data']):
                    try:
                        while(bool(after['data'])):
                            try:
                                for more_reaction in after['data']:
#                                    print('new reactions: ',more_reaction['id'])
                                    data[id_p].update({more_reaction['id']:{'name':more_reaction['name'],'type':more_reaction['type']}})
                                    if bool(after['data']):
                                       after = QUERY.request(id_p+'/reactions?limit=25&after='+after['paging']['cursors']['after'])
                            except NameError as e:
                                print("Error in paging reactions: ", e)
                    except Exception as e:
                        print("Error in: ", e)

    with open('react_data.json', 'w') as write_file:
        json.dump(data, write_file)


def comments_comm(id_comment):
    comment = QUERY.get_object(id=id_comment, fields='comments')
    data = {}
    if bool(comment.get('comments')):
        data.update({id_comment:{}})
        for msg in comment['comments']['data']:
            data[id_comment].update({msg['id']:{'name': msg['from']['name'], 'message':msg['message'], 'created_time':msg['created_time']}})
    return data
 
def comments(ids):
    data = {}
    print("Extract messages to post")
    for id_p in ids:
        comments_post = QUERY.get_object(id=id_p, fields='comments')
        data.update({id_p:{}})
        if(bool(comments_post.get('comments'))):
            for comment in comments_post['comments']['data']:
                comm_comm = comments_comm(comment['id'])
                data[id_p].update({comment['id']:{'name': comment['from']['name'],'message':comment['message'],'created_time':comment['created_time'],'comments':comm_comm}})
    with open('comments_data.json', 'w') as write_file:
        json.dump(data, write_file)

def main():
#    posts_ids =  published_post()
    posts_ids = ['194579180748613_1082570431949479', '194579180748613_1092444200962102']
#    reactions(posts_ids)
    comments(posts_ids)
if __name__=='__main__':
    main()






