from tkinter import *
import quick_projects.one_shots.mal_voice_acter.mal_api as mal
import copy
import os

def start():
    print(e1.get())
    print(e2.get())
    if episode_cap.get():
        print(e3.get())
    else:
        print("All episodes")
    if allow_airing.get():
        print("Currently Airing Allowed")
    else:
        print("Currently Airing Not Allowed")

    user_a = mal.read_animelist(e1.get())
    user_a = mal.filter_out_plan_to_watch(user_a)
    user_b = mal.read_animelist(e2.get())
    user_b = mal.filter_out_plan_to_watch(user_b)
    if not allow_airing.get():
        user_a = mal.filter_out_currently_airing(user_a)
        user_b = mal.filter_out_currently_airing(user_b)
    if episode_cap.get():
        user_a = mal.filter_out_long_series(user_a, e3.get())
        user_b = mal.filter_out_long_series(user_b, e3.get())

    shared = get_shared(user_a, user_b)  # gets anime that is shared and makes the rating to ratingA|ratingB
    user_a_exclusive = [x for x in user_a if x['series_title'] not in [y['series_title'] for y in user_b]]
    user_b_exclusive = [x for x in user_b if x['series_title'] not in [y['series_title'] for y in user_a]]

    write_html(shared, user_a_exclusive, user_b_exclusive)
    os.system("start "+'result.html')


def get_shared(user_a, list_b_anime):
    result = list()
    connector = '|'
    for list_a_anime in user_a:
        for m in list_b_anime:
            if list_a_anime['series_title'] == m['series_title']:
                to_be_added = copy.deepcopy(list_a_anime)
                # if a key starts with 'my' like 'my_score' then combine the values from the two dictionaries with
                # a connector.
                # for example if user_a has my_score = 4 and user_b has my_score = 6 then this will make my_score = 4|6
                for key in to_be_added.keys():
                    if key.startswith('my'):
                        to_be_added[key] = list_a_anime[key] + connector + m[key]
                result.append(to_be_added)
    return result



def write_html(shared, user_a_list, user_b_list):
    before = '''<style type="text/css">

table {
font-family: "Lato","sans-serif";	}		/* added custom font-family  */

table.one {
margin-bottom: 3em;
border-collapse:collapse;	}

td {							/* removed the border from the table data rows  */
text-align: center;
width: 10em;
padding: 1em; 		}

th {							  /* removed the border from the table heading row  */
text-align: center;
padding: 1em;
background-color: #e8503a;	     /* added a red background color to the heading cells  */
color: white;		}			      /* added a white font color to the heading text */

tr {
height: 1em;	}

table tr:nth-child(even) {		      /* added all even rows a #eee color  */
       background-color: #eee;		}

table tr:nth-child(odd) {		     /* added all odd rows a #fff color  */
background-color:#fff;		}


div.container p {
font-family: Arial;
font-size: 22px;
font-style: normal;
font-weight: bold;
text-decoration: none;
text-transform: none;
color: #e8503a;
background-color: #ffffff;
}
</style>
'''
    table_start = '''<table class="one">
    <div class="container">
    {}
    </div><tr>
    <th>Anime Title</th>
    <th>Type</th>
    <th>Episodes</th>
    <th>Score</th>
    </tr>'''
    table_end = '''</table>'''
    single_row = '''<tr>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    </tr>'''

    fo = open('result2.html', 'w', encoding='utf-8')
    fo.write(before)

    fo.write(table_start.format('''
    <p>Made by: Master3243</p>
    <p>-</p>
    <p>USER A: master3243</p>
    <p>USER B: otakuasim</p>
    <p>SHARED ANIME LIST :</p>'''))
    for anime in shared:
        cell1 = anime['series_title']
        cell2 = mal.get_series_type(anime['series_type'])
        cell3 = anime['my_watched_episodes'] + ' / ' + anime['series_episodes']
        cell4 = anime['my_score']
        fo.write(single_row.format(cell1, cell2, cell3, cell4))
    fo.write(table_end)

    fo.write(table_start.format(e1.get() + '\'S EXCLUSIVE ANIME LIST :'))
    for anime in user_a_list:
        cell1 = anime['series_title']
        cell2 = mal.get_series_type(anime['series_type'])
        cell3 = anime['my_watched_episodes'] + ' / ' + anime['series_episodes']
        cell4 = anime['my_score']
        fo.write(single_row.format(cell1, cell2, cell3, cell4))
    fo.write(table_end)

    fo.write(table_start.format(e2.get() + '\'S EXCLUSIVE ANIME LIST :'))
    for anime in user_b_list:
        cell1 = anime['series_title']
        cell2 = mal.get_series_type(anime['series_type'])
        cell3 = anime['my_watched_episodes'] + ' / ' + anime['series_episodes']
        cell4 = anime['my_score']
        fo.write(single_row.format(cell1, cell2, cell3, cell4))
    fo.write(table_end)
    # fo.write(table_start)
    # for anime in user_a_list:
    #     fo.write(single_row.format(*anime))
    # fo.write(table_end)
    #
    # fo.write(table_start)
    # for anime in user_b_list:
    #     fo.write(single_row.format(*anime))
    # fo.write(table_end)


if __name__ == '__main__':
    master = Tk()
    Label(master, text="Account A").grid(row=0)
    Label(master, text="Account B").grid(row=1)
    Label(master, text="").grid(row=2)
    Label(master, text="Num of episodes:").grid(row=3)
    Label(master, text="Include Currently Airing Anime:").grid(row=6)
    # Label(master, text="").grid(row=7)

    e1 = Entry(master)
    e2 = Entry(master)
    e3 = Entry(master)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=5, column=1)

    episode_cap = IntVar()
    r2 = Radiobutton(master, text="Set amount", value=True, variable=episode_cap,
                     command=lambda: e3.config(state=NORMAL))

    r1 = Radiobutton(master, text="Don't care", value=False, variable=episode_cap,
                     command=lambda: e3.config(state=DISABLED))
    r1.grid(row=4)
    r2.grid(row=5)
    e3.config(state=DISABLED)

    allow_airing = IntVar()
    c1 = Checkbutton(text="", variable=allow_airing,
                     onvalue=1, offvalue=0, anchor="w")
    c1.grid(row=6, column=1, sticky=W)

    Button(master, text='Generate', command=lambda: start()).grid(row=10, column=1, sticky=W, pady=4)

    mainloop()
