#!/usr/bin/env python3
"""Verify specification structure/fixtures; does not validate a deployed service."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
from urllib.parse import urlsplit, unquote
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / 'docs/specs'
NAMES = ['MEASUREMENT_SPEC.md', 'SAMPLING_AND_ESTIMATION_SPEC.md', 'SCORING_SPEC_V0.md', 'API_AND_STATE_MACHINE_SPEC.md', 'ARTIFACT_LINEAGE_AND_GOVERNANCE.md', 'PILOT_CALIBRATION_PROTOCOL.md', 'DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md']
checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

schema = json.loads((SPECS/'assessment_contract.schema.json').read_text())
Draft202012Validator.check_schema(schema)
check('json_schema_meta_validation', True)
def validate(name, payload):
    view = {'$schema':schema['$schema'], '$defs':schema['$defs'], '$ref':'#/$defs/'+name}
    return not list(Draft202012Validator(view).iter_errors(payload))

base = dict(result_id='synthetic-result', session_id='synthetic-session', result_version='test-1', status='scored', profile_id='baseline-design-v0.1', estimand='finite_frame_correct_response_total', count_unit='lemma_pos', frame_id='synthetic-frame', frame_size=10, estimate=4, interval={'type':'design_confidence','method':'hypergeometric_inversion_bonferroni','level':0.95,'bounds':[1,8],'conditional_on':['fixed_potential_outcomes','frozen_screening','valid_focused_sampling']},claim_status='diagnostic_only',public_vocabulary_claim_allowed=False,theta=None,vocabulary_count=None,cefr=None,reason_codes=[])
check('synthetic_scored_result_valid', validate('AssessmentResult',base))
for status, reason in [('insufficient_evidence','incomplete_design_responses'),('invalidated','item_key_invalidated')]:
    p=copy.deepcopy(base); p.update(status=status,estimate=None,interval=None,reason_codes=[reason])
    check(status+'_null_result_valid',validate('AssessmentResult',p))
    p['estimate']=1
    check(status+'_numeric_result_rejected',not validate('AssessmentResult',p))
for key,value in [('theta',1),('vocabulary_count',100),('cefr','B2'),('public_vocabulary_claim_allowed',True),('count_unit','word_family'),('estimand','latent_known_words'),('estimate',None),('interval',None),('unexpected',1)]:
    p=copy.deepcopy(base);p[key]=value
    check('reject_'+key,not validate('AssessmentResult',p))
submission={'expected_version':1,'presentation_id':'synthetic-presentation','answer':{'kind':'dont_know'}}
check('dont_know_submission_valid',validate('SubmitResponse',submission))
p=copy.deepcopy(submission);p['answer']['option_id']='synthetic-option'
check('dont_know_with_option_rejected',not validate('SubmitResponse',p))
p=copy.deepcopy(submission);p['answer']={'kind':'choice','option_id':'synthetic-option'}
check('choice_submission_valid',validate('SubmitResponse',p))
p['correct']=True
check('client_correctness_rejected',not validate('SubmitResponse',p))
check('unsupported_create_profile_rejected',not validate('CreateAssessment',{'profile_id':'cat-v0','form_id':'synthetic','locale':'en'}))

# Verify all local JSON references, including external OpenAPI schemas.
references=0
def pointer(document, fragment):
    result=document
    if fragment:
        if not fragment.startswith('/'):
            raise AssertionError('unsupported JSON fragment '+fragment)
        for token in fragment[1:].split('/'):
            result=result[token.replace('~1','/').replace('~0','~')]
    return result

def visit(value, path):
    global references
    if isinstance(value,dict):
        if '$ref' in value:
            url=urlsplit(value['$ref'])
            check('local_ref_'+str(references),not url.scheme and not url.netloc)
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            pointer(json.loads(target.read_text()),unquote(url.fragment))
            references+=1
        for child in value.values():visit(child,path)
    elif isinstance(value,list):
        for child in value:visit(child,path)
api_path=SPECS/'assessment.openapi.json'
api=json.loads(api_path.read_text())
visit(schema,SPECS/'assessment_contract.schema.json')
visit(api,api_path)
operations=[]
for path,item in api['paths'].items():
    for method,op in item.items():
        operations.append(op['operationId'])
        if method=='post':
            check(op['operationId']+'_idempotency_header',any(p['name']=='Idempotency-Key' and p['required'] for p in op.get('parameters',[])))
check('six_unique_http_operations',len(operations)==6 and len(set(operations))==6)
check('next_is_mutation_not_get','get' not in api['paths']['/v1/assessments/{session_id}/next'])
check('dont_know_and_no_score_shared_schema',schema['$defs']['Answer']['oneOf'][1]['properties']['kind']['const']=='dont_know' and 'insufficient_evidence' in schema['$defs']['AssessmentResult']['properties']['status']['enum'])

for name in NAMES:
    text=(SPECS/name).read_text()
    check(name+'_version_and_data', '2.0.0' in text and '42,497' in text and '3,885' in text)
    check(name+'_shared_contract_link','README.md)' in text)
for name in NAMES[:3]:
    text=(SPECS/name).read_text()
    check(name+'_baseline_estimand','finite_frame_correct_response_total' in text and 'baseline-design-v0.1' in text and 'lemma_pos' in text)

archive=ROOT/'raw/specs-before-harmonization'
manifest=json.loads((archive/'manifest.json').read_text())
check('eight_archived_files',len(manifest['files'])==8)
for entry in manifest['files']:
    check('archive_exact_'+entry['name'],hashlib.sha256((archive/entry['name']).read_bytes()).hexdigest()==entry['sha256'])
research=sorted(p.name for p in (ROOT/'raw').glob('[0-9][0-9]-*.md'))
check('75_numbered_research_documents',len(research)==75 and [int(n[:2]) for n in research]==list(range(1,76)))
matrix=(SPECS/'RESEARCH_INCORPORATION.md').read_text()
check('all_ten_new_research_files_traced',all(n in matrix for n in research if 66<=int(n[:2])<=75))

# Historical originals deliberately retain original-context links and bytes.
# Check current documents/research only; do not pretend old relative links were repaired.
files=[]
for folder in [ROOT/'docs',ROOT/'raw',ROOT/'tools']:
    files.extend(p for p in folder.rglob('*.md') if not (archive in p.parents and p.name!='README.md'))
files += [ROOT/'README.md',ROOT/'ROADMAP_ARCHITECTURE.md']
links=0
for path in files:
    for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+[^)]*)?\)',path.read_text()):
        u=urlsplit(target)
        if u.scheme or u.netloc or not u.path:continue
        links+=1
        resolved=path.parent/unquote(u.path)
        if not resolved.exists():raise AssertionError('broken local link: '+str(path.relative_to(ROOT))+' -> '+target)
check('active_local_link_targets_exist',links>0)
print(json.dumps({'status':'PASS','checks_passed':len(checks),'json_references_resolved':references,'http_operations':len(operations),'p0_specs_verified':len(NAMES),'numbered_research_files':len(research),'archive_files_hash_verified':len(manifest['files']),'local_link_targets_checked':links,'excluded_link_context':'eight byte-preserved historical specs/roadmap; original relative links are historical','scope':'schema fixtures, shared tokens, archive preservation and local target paths; not OpenAPI meta-schema certification, business invariants, source audit, service deployment or empirical validation'},indent=2))
