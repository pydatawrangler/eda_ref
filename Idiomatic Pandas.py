# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python [conda env:pandas_env]
#     language: python
#     name: conda-env-pandas_env-py
# ---

# # Idiomatic Pandas
#
# © MetaSnake 2022, CC BY-NC

# +
import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# +
# # !pip install pandas matplotlib
# -


pd.__version__

# + jupyter={"outputs_hidden": true} tags=[]
pd.show_versions()
# -

# ## Loading Data

# !ls *.csv

data = [pd.read_csv(f, parse_dates=['time'], na_values='-') for f in glob.glob('tweet_activity_metrics___mharrison___*')]
df = pd.concat(data, ignore_index=True).sort_values('time')
df

df.to_csv('__mharrison__2020-2021.csv', index=False)

pd.read_csv('__mharrison__2020-2021.csv')







# ## Load data from Web

url = 'https://github.com/mattharrison/datasets/raw/master/data/__mharrison__2020-2021.csv'
df = pd.read_csv(url, parse_dates=['time'])

df

# ## Load Data Exercise
#
# * Load the data using the cell above.
# * If you can't do this please alert!









# ## Exploring
#
# Definitions
#
# * *Impressions* - Number of times people saw the tweet
# * *Engagements* - Number of "interactions" (clicks, replies, retweets, likes)
# * *Engagement rate* - Engagements divided by impressions

df.T

df.shape

df.dtypes

pd.options.display.max_columns

from IPython.display import display
with pd.option_context('display.max_columns', 240):
    display(df)

df.isna().sum()

# ## Explore Exercise
# * Use `.describe` to view the summary statistics
# * Use `.corr` to view column correlations

df.describe()

df.corr()





# ## Types

df.dtypes

df.memory_usage()

df.memory_usage(deep=True)

df.memory_usage(deep=True).sum()

(df
 .select_dtypes(int).describe()
)

(df
 #.select_dtypes(float)
 .select_dtypes('float64')
 .describe()
)

(df
 .assign(impressions=df.impressions.astype(int),
         engagements=df.engagements.astype(int)
         # lots of this here
        )
)

(df
 .impressions
 .astype(int))

# +
# df.assign?
# -

# also note
(df
 .assign(impressions=df.impressions.astype(int),
         engagement rate=df.engagements rate.astype(int)
         # lots of this here
        )
)

# fix names
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
)

df.filter(regex=r'promoted')

(df
 .drop(columns=[c for c in df.columns if 'promoted' in c])
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .describe()
)

# be careful with renaming
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .drop(columns=[c for c in df.columns if 'promoted' in c])
)


# +
# df.drop?

# +
def drop_col(df_, pattern):
     return df_.drop(columns=[c for c in df_.columns if pattern in c])

(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 #.pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .pipe(drop_col, pattern='promoted')
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
)

# +

(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .memory_usage(deep=True)
 .sum()  # 3 megs
)
# +
# df.pipe?
# -
# ## Column Cleanup Exercise
# (Please don't mutate here!)
#
# * Use `.loc` to select the *impressions* and *engagement* columns
# * Use `.drop` to select the *impressions* and *engagement* columns
# * Use `.rename` to rename *impressions* to *imp* and *engagement* to *eng*














# ## Ok, Types for real

# +

(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .describe()
)
# -

np.iinfo('int64')

for size in ['uint8', 'uint16', 'uint32', 'int8', 'int16', 'int32', 'int64']:
    print(f'{size=} {np.iinfo(size)}')

# +

(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
        )
 .describe()
)
# -

kwargs = {}
for col in df.select_dtypes(float).columns:
    print(col)
    kwargs[col] = df[col].astype(int)
kwargs

# use dict comp if you don't want to type every column
# assign w/ dict comp. and lambda
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']}  # less than 255
        )
)

# why c=c?
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']}  # less than 65,535
        )
 #.corr()
 .describe()
)

# https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
squares = []
for x in range(5):
    squares.append(lambda: x**2)
for s in squares:
    print(s())

# https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
squares = []
for x in range(5):
    squares.append(lambda x=x: x**2)
for s in squares:
    print(s())

(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']}  # less than 65,535
        )
 .describe()
)

(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']}  # less than 65,535
         
        )
 .memory_usage(deep=True) 
 .sum()  # was 3 megs
)

# most is from text
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['Tweet_id', 'permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']}  # less than 65,535
         
        )
 .memory_usage(deep=True) 
 .pipe(lambda ser: ser/ser.sum()*100)
# .sum()  # was 3 megs
)

# convert first part of permalink to category and add back tweet_id
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
         Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                               index=df_.index),
        )
 .memory_usage(deep=True) 
 .sum()  # was 3 megs
)





# convert first part of permalink to category and add back tweet_id
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
         Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                               index=df_.index),
        )
 .describe()
 #.memory_usage(deep=True) 
 #.sum()  # was 3 megs
)




# ## Alternate Integer Conversion Exercise
# (Again, no mutation!)
#
# * Use `.select_dtypes` to filter all `int` columns from `df`
# * Use `.astype` with above to convert all columns to `uint8`
# * Use `.assign` with above to create new dataframe with updated integer columns









# ## Other Types
# Can apply similar logic to floats, and strings.
#
# Converting "Tweet_text" to a category doesn't make sense because it is high cardinality

# Uses MORE memory if tweet text is a category!
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
         Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                               index=df_.index),
         Tweet_text=lambda df_:df_.Tweet_text.astype('category')
        )
 .memory_usage(deep=True) 
 .sum()  # was 3 megs
)

# ## Other types Exercise
# * Use the `%%timeit` cell magic to see how long it takes to run `.str.lower()` on the original *Tweet permalink* column
# * Create a new dataframe, `df2`, with our current chain
# * Use the `%%timeit` cell magic to see how long it takes to run `.str.lower()` on the *df2.Tweet_permalink* column











# ## Dates

(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
         Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                               index=df_.index),
        )
 .time
)

# Convert to Local Time (already in UTC)
(df
 .rename(columns=lambda col_name: col_name.replace(' ', '_'))
 .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
 .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
 .astype({c:'uint8' for c in ['replies', 'hashtag_clicks', 'follows']})  # less than 255)
 .assign(impressions=df.impressions.astype('uint32'),
         engagements=df.engagements.astype('uint16'),
         #**{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
         **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                          'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
         Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                               index=df_.index),
         time=lambda df_: df_.time.dt.tz_convert('America/Denver')
        )
 .time
)

# ## Dates Exercise
# * Create a series with the months of the *time* column
# * Convert the *time* column to UTC
# * Convert the *time* column to `America/New_York`









# ## Chain
#
# Chaining is also called "flow" programming. Rather than making intermediate variables, just leverage the fact that most operations return a new object and work on that.
#
# The chain should read like a recipe of ordered steps.
#
# (BTW, this is actually what we did above.)
#
# <div class='alert alert-warning'>
#     Hint: Leverage <tt>.pipe</tt> if you can't find a way to chain 😉🐼💪
# </div>

# convert to a function
def tweak_twitter(df):
    return (df
     .rename(columns=lambda col_name: col_name.replace(' ', '_'))
     .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
     .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
     .assign(impressions=df.impressions.astype('uint32'),
             engagements=df.engagements.astype('uint16'),
             **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
             **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                              'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
             Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                                   index=df_.index),
             time=lambda df_: df_.time.dt.tz_convert('America/Denver')
            )
    )



# +
# I would want my notebook to start off like this:
import glob

import numpy as np
import pandas as pd

data = [pd.read_csv(f, parse_dates=['time'], na_values='-') for f in glob.glob('tweet_activity_metrics___mharrison___*')]
df = pd.concat(data, ignore_index=True).sort_values('time')


# -

def tweak_twitter(df):
    return (df
     .rename(columns=lambda col_name: col_name.replace(' ', '_'))
     .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
     .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
     .assign(impressions=df.impressions.astype('uint32'),
             engagements=df.engagements.astype('uint16'),
             **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
             **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                              'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
             Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                                   index=df_.index),
             time=lambda df_: df_.time.dt.tz_convert('America/Denver')
            )
    )
twit_df = tweak_twitter(df)

# compare with non-chain
df1 = df.rename(columns=lambda col_name: col_name.replace(' ', '_'))
keep = [c for c in df1.columns if 'promoted' not in c]
df2 = df1[keep]
keep2 = [c for c in df2 if c not in ['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone']]
df3 = df2[keep2]
imps = df3.impressions.astype('uint32')
df3.impressions = imps
eng = df3.engagements.astype('uint16')
df3['engagements'] = eng
df3['replies'] = df3.replies.astype('uint8')
df3['hashtag_clicks'] = df3.hashtag_clicks.astype('uint8')


# +
# easy to debug
#  - assign to var (renamed_df)
#  - comment out
#  - pipe to display

from IPython.display import display

def get_var(df, var_name):
    globals()[var_name] = df
    return df

def tweak_twitter(df):
    return (df
     .rename(columns=lambda col_name: col_name.replace(' ', '_'))
     .pipe(get_var, 'renamed_df')
     .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
     .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
     .pipe(lambda df_:display(df_) or df_)
     .assign(impressions=df.impressions.astype('uint32'),
             engagements=df.engagements.astype('uint16'),
             **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
             **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                            'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
             Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                                   index=df_.index),
            time=lambda df_: df_.time.dt.tz_convert('America/Denver')
            )
    )
twit_df = tweak_twitter(df)
# -

renamed_df








def tweak_twitter(df):
    return (df
     .rename(columns=lambda col_name: col_name.replace(' ', '_'))
     .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
     .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
     .assign(impressions=df.impressions.astype('uint32'),
             engagements=df.engagements.astype('uint16'),
             **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
             **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                              'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
             Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                                   index=df_.index),
             time=lambda df_: df_.time.dt.tz_convert('America/Denver')
            )
    )
twit_df = tweak_twitter(df)

# ## Chain Exercise
# * Use `.pipe` to print the shape of the dataframe after every step in the chain of the `tweak_twitter` function









# ## Don't Mutate
#
# > "you are missing the point, inplace rarely actually does something inplace, you are thinking that you are saving memory but you are not."
# >
# > **jreback** - Pandas core dev
#
#
#
# https://github.com/pandas-dev/pandas/issues/16529#issuecomment-676518136
#
# * In general, no performance benefits
# * Prohibits chaining
# * ``SettingWithCopyWarning`` fun













# ## Don't Apply (if you can)

def tweak_twitter(df):
    return (df
     .rename(columns=lambda col_name: col_name.replace(' ', '_'))
     .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
     .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
     .assign(impressions=df.impressions.astype('uint32'),
             engagements=df.engagements.astype('uint16'),
             **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
             **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                              'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
             Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                                   index=df_.index),
             time=lambda df_: df_.time.dt.tz_convert('America/Denver')
            )
    )
twit_df = tweak_twitter(df)

twit_df


def to_percent(val):
    return val * 100
twit_df.engagement_rate.apply(to_percent)

# same result
twit_df.engagement_rate * 100


# %%timeit
# however ...
twit_df.engagement_rate.apply(to_percent)

# %%timeit
twit_df.engagement_rate * 100

# 14X slower!
1008 / 71

# How would we check if text had unicode?
'Hello \U0001f600'.encode('ascii', errors='replace').decode('ascii')

'Hello \U0001f600'.encode('utf8', errors='replace').decode('utf8')


# +
# story is a little different with text

def is_unicode(val):
    return val.encode('ascii', errors='replace').decode('ascii') != val


# -

# %lsmagic

# %%timeit?

# %%timeit
twit_df.Tweet_text.apply(is_unicode)

# %%timeit
twit_df.Tweet_text.str.encode('ascii', errors='replace').str.decode('ascii') == twit_df.Tweet_text

# %%timeit
twit_df.Tweet_text.str.startswith('@')


def startswith_at(txt):
    return txt.startswith('@')


# %%timeit
twit_df.Tweet_text.apply(startswith_at)


def tweak_twitter(df):
    return (df
     .rename(columns=lambda col_name: col_name.replace(' ', '_'))
     .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns if 'promoted' in c]))
     .drop(columns=['permalink_clicks', 'app_opens', 'app_installs', 'email_tweet', 'dial_phone'])
     .assign(impressions=df.impressions.astype('uint32'),
             engagements=df.engagements.astype('uint16'),
             **{c:lambda df_, c=c:df_[c].astype('uint8') for c in ['replies', 'hashtag_clicks', 'follows']},  # less than 255
             **{c:lambda df_, c=c:df_[c].astype('uint16') for c in ['retweets', 'likes', 'user_profile_clicks', 'url_clicks', 
                                              'detail_expands', 'media_views', 'media_engagements']},  # less than 65,535
             Tweet_permalink=lambda df_: pd.Series('https://twitter.com/__mharrison__/status/', dtype='category', 
                                                   index=df_.index),
             time=lambda df_: df_.time.dt.tz_convert('America/Denver'),
             is_reply=lambda df_: df_.Tweet_text.str.startswith('@'),
             length=lambda df_:df_.Tweet_text.str.len(),
             num_words=lambda df_:df_.Tweet_text.str.split().apply(len),
             is_unicode=lambda df_:df_.Tweet_text.str.encode('ascii', errors='replace').str.decode('ascii') != df_.Tweet_text,
             hour=lambda df_:df_.time.dt.hour,
             dom=lambda df_:df_.time.dt.day,  #day of month
             dow=lambda df_:df_.time.dt.dayofweek,  #day of week
             at_tweet=lambda df_:df_.Tweet_text.str.contains('@'),
             has_newlines=lambda df_:df_.Tweet_text.str.contains('\n'),
             num_lines=lambda df_:df_.Tweet_text.str.count('\n'),
             num_mentions=lambda df_:df_.Tweet_text.str.count('@'),
             has_hashtag=lambda df_:df_.Tweet_text.str.count('#'),
            )
    )
twit_df = tweak_twitter(df)

twit_df

# ## Apply Exercise
# * Calculate engagement ratio by dividing *engagements* by *impressions*
# * Calculate engagement ratio 2 by dividing the sum of *replies*, *retweets*, *likes*, *user_profile_clicks*, and *detail_expands* by *impressions*




















# ## Master Aggregation

(twit_df
 .groupby(twit_df.time.dt.year)
 .mean()
)

twit_df.groupby(twit_df.time.dt.year).mean()


(twit_df
 .groupby(twit_df.time.dt.year)
 .impressions
 .mean()
)

# %%timeit
(twit_df
 .groupby(twit_df.time.dt.year)
 .mean()
 [['impressions', 'replies']]  # index operation with a list inside 
)

# %%timeit
(twit_df
 .groupby(twit_df.time.dt.year)
 [['impressions', 'replies']]  # index operation with a list inside 
  .mean()
)

twit_df.Tweet_text.str.

twit_df.time.dt.year.rename('year')

pd.options.display.float_format

# +
(twit_df
 .groupby([twit_df.time.dt.year.rename('year'), twit_df.time.dt.month.rename('month')])
 [['impressions', 'replies']]
 .mean()
 #.round(2)
 .style
 .format({'replies': '{:.3f}', 'impressions': '{:e}'})
 
)
# -

(twit_df
 .groupby([twit_df.time.dt.year, twit_df.time.dt.month])
 [['impressions', 'replies']]
 #.mean()
 .median()
 .plot()
)

(twit_df
 #.groupby([twit_df.time.dt.year, twit_df.time.dt.month])
 .groupby(pd.Grouper(key='time', freq='2M'))
 [['impressions', 'replies']]
 #.mean()
 .median()
 .plot()
)

(twit_df
 #.groupby([twit_df.time.dt.year, twit_df.time.dt.month])
 .groupby(pd.Grouper(key='time', freq='2w'))
 [['impressions', 'replies']]
 .mean()
 .plot()
)

(twit_df
 #.groupby([twit_df.time.dt.year, twit_df.time.dt.month])
 .groupby(pd.Grouper(key='time', freq='7d5h'))
 [['impressions', 'replies']]
 .mean()
 #.plot()
)

(twit_df
 #.groupby([twit_df.time.dt.year, twit_df.time.dt.month])
 .groupby([pd.Grouper(key='time', freq='7d5h'), 'is_unicode'])
 [['impressions', 'replies']]
 .mean()
 #.plot()
)


# +
# multiple aggregates
def second_to_last(ser):
    try:
        return ser.iloc[-2]
    except IndexError:
        return 0

(twit_df
 .groupby([pd.Grouper(key='time', freq='7d5h'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
)

# +
# multiple aggregates

(twit_df
 .groupby([pd.Grouper(key='time', freq='7d5h'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .plot()
)

# +
# multiple aggregates

(twit_df
 .groupby([pd.Grouper(key='time', freq='7d'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .unstack()
)

# +
# multiple aggregates

(twit_df
 .groupby([pd.Grouper(key='time', freq='7d'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .unstack()
 .impressions
)
# -

# multiple aggregates
(twit_df
 .groupby([pd.Grouper(key='time', freq='7d'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .unstack()
 .impressions
 ['mean']  # note have to use index syntax here
)

# multiple aggregates
(twit_df
 .groupby([pd.Grouper(key='time', freq='7d'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .unstack()
 .impressions
 .mean  # note have to use index syntax here
)

# multiple aggregates
(twit_df
 .groupby([pd.Grouper(key='time', freq='7d'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .unstack()
 .impressions
 ['mean']
 .plot()
)

# multiple aggregates
# dealing with missing values
(twit_df
 .groupby([pd.Grouper(key='time', freq='7d'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .unstack()
 .impressions
 ['mean']
 #.fillna(0)
 #.interpolate()
 #.bfill()
 #.dropna()
 .loc['2021/07':'2021/08']
 #.plot()
)

# multiple aggregates
(twit_df
 .groupby([pd.Grouper(key='time', freq='3d'), 'is_unicode'])
 [['impressions', 'replies']]
 .agg(['mean', 'median', second_to_last])
 .unstack()
 .impressions
 ['mean']
 .interpolate()
 .rolling(7)
 .mean()
 .plot()
)

# +
# named aggregation

(twit_df
 .groupby([pd.Grouper(key='time', freq='M'), 'is_unicode'])
 .agg(total_views=('impressions', 'sum'),
     mean_views=('impressions', 'mean'),
     profile_clicks=('user_profile_clicks', lambda ser: ser.sum()))
)

# +
# named aggregation - fails with resample

(twit_df
 #.groupby([pd.Grouper(key='time', freq='M'), 'is_unicode'])
 .set_index('time')
 .resample('M')
 .agg(total_views=('impressions', 'sum'),
     mean_views=('impressions', 'mean'),
     profile_clicks=('user_profile_clicks', lambda ser: ser.sum()))
)

# +
# named aggregation

(twit_df
 .groupby([pd.Grouper(key='time', freq='M'), 'is_unicode'])
 .agg(total_views=('impressions', 'sum'),
     mean_views=('impressions', 'mean'),
     profile_clicks=('user_profile_clicks', lambda ser: ser.sum()))
 .unstack()
 .profile_clicks
 .plot()
)
# -
# ## Aggregation Exercise
# * What were the total impressions for each year?
# * What were the total impressions for each month?
# * Plot the previous
# * What were the total impressions for unicode and non-unicode tweets for each month?
# * Plot the previous
# * What were the total impressions for reply and non-reply tweets for each month?
# * Plot the previous









# ## Summary
#
# * Correct types save space and enable convenient math, string, and date functionality
# * Chaining operations will:
#    * Make code readable
#    * Remove bugs
#    * Easier to debug
# * Don't mutate (there's no point). Embrace chaining.
# * ``.apply`` is slow for math
# * Aggregations are powerful. Play with them until they make sense
#
# Connect with me on LinkedIn or Twitter (@\_\_mharrison\_\_)


