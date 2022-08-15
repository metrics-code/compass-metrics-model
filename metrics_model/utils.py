import math

BACKOFF_FACTOR = 0.2
MAX_RETRIES = 21
MAX_RETRIES_ON_REDIRECT = 5
MAX_RETRIES_ON_READ = 8
MAX_RETRIES_ON_CONNECT = 21
STATUS_FORCE_LIST = [408, 409, 429, 502, 503, 504]
METADATA_FILTER_RAW = 'metadata__filter_raw'
REPO_LABELS = 'repository_labels'


COMMIT_FREQUENCY_WEIGHT_ACTIVITY = 0.18009
UPDATED_SINCE_WEIGHT_ACTIVITY = -0.12742
MAINTAINER_COUT_ACTIVITY = 0.2090
CODE_REVIEW_COUNT_WEIGHT_ACTIVITY = 0.04919
CLOSED_ISSUES_WEIGHT_ACTIVITY = 0.04919
UPDATED_ISSUES_WEIGHT_ACTIVITY = 0.04919
COMMENT_FREQUENCY_WEIGHT_ACTIVITY = 0.07768
CONTRIBUTOR_COUNT_WEIGHT_ACTIVITY = 0.18009
ORG_COUNT_WEIGHT_ACTIVITY = 0.11501
RECENT_RELEASES_WEIGHT_ACTIVITY = 0.03177
CREATED_SINCE_WEIGHT_ACTIVITY = 0.07768
MEETING_ACTIVITY = 0.02090
MEETING_ATTENDEE_COUNT_ACTIVITY = 0.02090


# Max thresholds for various parameters.
CODE_REVIEW_COUNT_THRESHOLD_ACTIVITY = 5 
CREATED_SINCE_THRESHOLD_ACTIVITY = 120
UPDATED_SINCE_THRESHOLD_ACTIVITY = 0.25
CONTRIBUTOR_COUNT_THRESHOLD_ACTIVITY = 2000
ORG_COUNT_THRESHOLD_ACTIVITY = 10
COMMIT_FREQUENCY_THRESHOLD_ACTIVITY = 1000
RECENT_RELEASES_THRESHOLD_ACTIVITY = 26
CLOSED_ISSUES_THRESHOLD_ACTIVITY = 5000
UPDATED_ISSUES_THRESHOLD_ACTIVITY = 5000
COMMENT_FREQUENCY_THRESHOLD_ACTIVITY = 5
DEPENDENTS_COUNT_THRESHOLD_ACTIVITY = 500000

ISSUE_FIRST_RESPONSE_WEIGHT_COMMUNITY = -0.1437
ISSUE_OPEN_TIME_WEIGHT_COMMUNITY = -0.1288
PR_OPEN_TIME_WEIGHT_COMMUNITY = -0.1288
COMMENT_FREQUENCY_WEIGHT_COMMUNITY = 0.1022
UPDATED_ISSUES_WEIGHT_COMMUNITY = 0.1972
CODE_REVIEW_WEIGHT_COMMUNITY = 0.1022
CLOSED_PRS_WEIGHT_COMMUNITY = 0.1972

ISSUE_FIRST_RESPONSE_THRESHOLD_COMMUNITY = 15
ISSUE_OPEN_TIME_THRESHOLD_COMMUNITY = 60
CI_BUILD_TIME_THRESHOLD_COMMUNITY = 0
CLOSED_PR_TIME_THRESHOLD_COMMUNITY = 90
PR_OPEN_TIME_THRESHOLD_COMMUNITY = 30
MAIL_THREAD_OUT_THRESHOLD_COMMUNITY = 0
EVENT_COUNT_THRESHOLD_COMMUNITY = 0
COMMENT_FREQUENCY_THRESHOLD_COMMUNITY = 5
UPDATED_ISSUES_THRESHOLD_COMMUNITY = 2000
CODE_REVIEW_THRESHOLD_COMMUNITY = 8
CLOSED_PRS_THRESHOLD_COMMUNITY = 4500

MIN_ACTIVITY_SCORE = -0.23786
MAX_ACTIVITY_SCORE = 1.23786
MIN_COMMUNITY_SCORE = -2.0319
MAX_COMMUNITY_SCORE = 3.03189


def normalize(score, min_score, max_score):
    return (score-min_score)/(max_score-min_score)

def get_param_score(param, max_value, weight=1):
    """Return paramater score given its current value, max value and
    parameter weight."""
    return (math.log(1 + param) / math.log(1 + max(param, max_value))) * weight

def perserve_model(item):
    total_weight_PRESERVE  = ( D1_COUNT_WEIGHT_PRESERVE + D2_COUNT_WEIGHT_PRESERVE + D1_D2_CONVERSION_RATE_WEIGHT_PRESERVE  )
    perserve_model_score = round(  
                        ((get_param_score(item["contributor_count"],
                                        D1_COUNT_THRESHOLD_PRESERVE, D1_COUNT_WEIGHT_PRESERVE)) +
                        (get_param_score(item["contributor_count_D2"],
                                        D2_COUNT_THRESHOLD_PRESERVE, D2_COUNT_WEIGHT_PRESERVE)) +
                        (get_param_score(item["D1-D2-conversion-rate"],
                                        D1_D2_CONVERSION_RATE_THRESHOLD_PRESERVE,
                                        D1_D2_CONVERSION_RATE_WEIGHT_PRESERVE))) /
                        total_weight_PRESERVE, 5)
    return perserve_model_score

def get_activity_score(item): 
    total_weight_ACTIVITY  = ( CREATED_SINCE_WEIGHT_ACTIVITY + UPDATED_SINCE_WEIGHT_ACTIVITY +
                                CONTRIBUTOR_COUNT_WEIGHT_ACTIVITY + 
                                COMMIT_FREQUENCY_WEIGHT_ACTIVITY + CODE_REVIEW_COUNT_WEIGHT_ACTIVITY +
                                CLOSED_ISSUES_WEIGHT_ACTIVITY + UPDATED_ISSUES_WEIGHT_ACTIVITY +
                                COMMENT_FREQUENCY_WEIGHT_ACTIVITY )
    activity_score = round(  
                            ((get_param_score(item["created_since"],
                                            CREATED_SINCE_THRESHOLD_ACTIVITY, CREATED_SINCE_WEIGHT_ACTIVITY)) +
                            (get_param_score(item["updated_since"],
                                            UPDATED_SINCE_THRESHOLD_ACTIVITY, UPDATED_SINCE_WEIGHT_ACTIVITY)) +
                            (get_param_score(item["contributor_count"],
                                            CONTRIBUTOR_COUNT_THRESHOLD_ACTIVITY,
                                            CONTRIBUTOR_COUNT_WEIGHT_ACTIVITY)) +                   
                            (get_param_score(item["commit_frequency"],
                                            COMMIT_FREQUENCY_THRESHOLD_ACTIVITY,
                                            COMMIT_FREQUENCY_WEIGHT_ACTIVITY)) +                
                            (get_param_score(item["closed_issues_count"],
                                            CLOSED_ISSUES_THRESHOLD_ACTIVITY, CLOSED_ISSUES_WEIGHT_ACTIVITY)) +
                            (get_param_score(item["updated_issues_count"],
                                            UPDATED_ISSUES_THRESHOLD_ACTIVITY, UPDATED_ISSUES_WEIGHT_ACTIVITY))+
                            (get_param_score(item["code_review_count"],
                                            CODE_REVIEW_COUNT_THRESHOLD_ACTIVITY, CODE_REVIEW_COUNT_WEIGHT_ACTIVITY)) +
                            (get_param_score(item["comment_frequency"],
                                            COMMENT_FREQUENCY_THRESHOLD_ACTIVITY, COMMENT_FREQUENCY_WEIGHT_ACTIVITY))) /
                            total_weight_ACTIVITY, 5)
    return normalize(activity_score, MIN_ACTIVITY_SCORE, MAX_ACTIVITY_SCORE)

def community_support(item):
    for i in ["issue_first_reponse_avg",  "issue_open_time_avg", "pr_open_time_avg"]:
        if not item[i]:
            return None
    total_weight_COMMUNITY = ISSUE_FIRST_RESPONSE_WEIGHT_COMMUNITY + ISSUE_OPEN_TIME_WEIGHT_COMMUNITY + PR_OPEN_TIME_WEIGHT_COMMUNITY + \
        COMMENT_FREQUENCY_WEIGHT_COMMUNITY + UPDATED_ISSUES_WEIGHT_COMMUNITY + \
        CODE_REVIEW_WEIGHT_COMMUNITY + CLOSED_PRS_WEIGHT_COMMUNITY
    score = round(
                ((get_param_score(item["issue_first_reponse_avg"],
                                ISSUE_FIRST_RESPONSE_THRESHOLD_COMMUNITY , ISSUE_FIRST_RESPONSE_WEIGHT_COMMUNITY*0.5)) +
                (get_param_score(item["issue_first_reponse_mid"],
                                ISSUE_FIRST_RESPONSE_THRESHOLD_COMMUNITY,
                                ISSUE_FIRST_RESPONSE_WEIGHT_COMMUNITY*0.5))+
                (get_param_score(item["issue_open_time_avg"],
                                ISSUE_OPEN_TIME_THRESHOLD_COMMUNITY,
                                ISSUE_OPEN_TIME_WEIGHT_COMMUNITY*0.5))+
                (get_param_score(item["issue_open_time_mid"],
                                ISSUE_OPEN_TIME_THRESHOLD_COMMUNITY,
                                ISSUE_OPEN_TIME_WEIGHT_COMMUNITY*0.5))+
                (get_param_score(item["pr_open_time_avg"],
                                PR_OPEN_TIME_THRESHOLD_COMMUNITY,
                                PR_OPEN_TIME_WEIGHT_COMMUNITY*0.5))+
                (get_param_score(item["pr_open_time_mid"],
                                PR_OPEN_TIME_THRESHOLD_COMMUNITY,
                                PR_OPEN_TIME_WEIGHT_COMMUNITY*0.5))+
                (get_param_score(item["comment_frequency"],
                                COMMENT_FREQUENCY_THRESHOLD_COMMUNITY, COMMENT_FREQUENCY_WEIGHT_COMMUNITY))+
                (get_param_score(item["updated_issues_count"],
                                UPDATED_ISSUES_THRESHOLD_COMMUNITY, UPDATED_ISSUES_WEIGHT_COMMUNITY))+
                (get_param_score(item["code_review_count"],
                                CODE_REVIEW_THRESHOLD_COMMUNITY, CODE_REVIEW_WEIGHT_COMMUNITY)) +
                (get_param_score(item["closed_prs_count"],
                                CLOSED_PRS_THRESHOLD_COMMUNITY, CLOSED_PRS_WEIGHT_COMMUNITY)))/
                total_weight_COMMUNITY, 5)
    return normalize(score, MIN_COMMUNITY_SCORE, MAX_COMMUNITY_SCORE)