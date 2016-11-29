# -*- coding: utf-8 -*-

import logging

from read.TranskribusPyClient.test import _colId_A
from read.TranskribusPyClient.client import TranskribusClient, getStoredCredentials

login, pwd = getStoredCredentials()

conn = TranskribusClient(proxies={'https':'http://cornillon:8000'}
                         , loggingLevel=logging.INFO)

sessionID = conn.auth_login(login, pwd)
doc = conn.collections_listEditDeclFeats(_colId_A)
doc.saveFormatFileEnc("-", "UTF-8", True)
conn.xmlFreeDoc(doc)

print conn.auth_logout()

"""
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<edFeatures>
  <edFeature>
    <featureId>1</featureId>
    <title>Long S</title>
    <description>Source uses long "s"</description>
    <optionList>
      <options>
        <optionId>1</optionId>
        <featureId>1</featureId>
        <text>Long s is normalized to "s"</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>2</optionId>
        <featureId>1</featureId>
        <text>Long s is transcribed as "ſ" U+017F "Latin small letter long s"</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>2</featureId>
    <title>u and v</title>
    <description>Source uses v for u</description>
    <optionList>
      <options>
        <optionId>3</optionId>
        <featureId>2</featureId>
        <text>Transcribed as in source</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>4</optionId>
        <featureId>2</featureId>
        <text>Transcribed according to modern spelling</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>3</featureId>
    <title>i and j</title>
    <description>Source uses "i" and "j" differently to modern spelling</description>
    <optionList>
      <options>
        <optionId>7</optionId>
        <featureId>3</featureId>
        <text>Normalized according to modern lexicon</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>5</optionId>
        <featureId>3</featureId>
        <text>Transcribed as in source</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>279</optionId>
        <featureId>3</featureId>
        <text>Capital letter "J" is normalized to "I" at the beginning of a word</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>5</featureId>
    <title>Printspace</title>
    <description>The printspace indicates the overall text region.</description>
    <optionList>
      <options>
        <optionId>9</optionId>
        <featureId>5</featureId>
        <text>Created by FineReader</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>8</optionId>
        <featureId>5</featureId>
        <text>Manually corrected</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>6</featureId>
    <title>Ligature "sz"</title>
    <description>"sz" is set as ligature</description>
    <optionList>
      <options>
        <optionId>10</optionId>
        <featureId>6</featureId>
        <text>Transcribed as "sz"</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>11</optionId>
        <featureId>6</featureId>
        <text>Normalized to "ß"</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>28</featureId>
    <title>Text regions</title>
    <description>Regions which contain handwritten text</description>
    <optionList>
      <options>
        <optionId>34</optionId>
        <featureId>28</featureId>
        <text>Manually corrected</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>33</optionId>
        <featureId>28</featureId>
        <text>Automatically created</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>29</featureId>
    <title>Line Regions</title>
    <description>Contain the text of line</description>
    <optionList>
      <options>
        <optionId>35</optionId>
        <featureId>29</featureId>
        <text>Automatically created</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>36</optionId>
        <featureId>29</featureId>
        <text>Manually corrected</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>30</featureId>
    <title>Baselines</title>
    <description>The baseline is defined as in Wikipedia - characters are "sitting" on the baseline</description>
    <optionList>
      <options>
        <optionId>38</optionId>
        <featureId>30</featureId>
        <text>Manually corrected</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>37</optionId>
        <featureId>30</featureId>
        <text>Automatically created</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>47</featureId>
    <title>Omitted text</title>
    <description>Even in diplomatic transcriptions the editor may decide to not transcribe specific notes or marginalia which do not contribute to the overall objective of the transcription</description>
    <optionList>
      <options>
        <optionId>59</optionId>
        <featureId>47</featureId>
        <text>Some text was omitted, e.g. marginalia, notes of librarians</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>60</optionId>
        <featureId>47</featureId>
        <text>No text was omitted</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>48</featureId>
    <title>Person names</title>
    <description>Tagging of person names</description>
    <optionList>
      <options>
        <optionId>61</optionId>
        <featureId>48</featureId>
        <text>Person names were tagged</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>62</optionId>
        <featureId>48</featureId>
        <text>Person names were not tagged</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>49</featureId>
    <title>Geo-Names</title>
    <description>Tagging of geo-names</description>
    <optionList>
      <options>
        <optionId>63</optionId>
        <featureId>49</featureId>
        <text>Geo-names were tagged</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>64</optionId>
        <featureId>49</featureId>
        <text>Geo-names wer not tagged</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>50</featureId>
    <title>Abbreviations - common</title>
    <description>Common abbreviations are usually known to most readers of a text, for example: e.g., i.e., &amp;, etc.</description>
    <optionList>
      <options>
        <optionId>65</optionId>
        <featureId>50</featureId>
        <text>Common abbreviations were not expanded</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>66</optionId>
        <featureId>50</featureId>
        <text>Common abbreviations were expanded</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>51</featureId>
    <title>Abbreviations</title>
    <description>Especially in medieval texts and early modern handwritting many words are abbreviated, or even characters are left out in the middle of a word. These abbreviations often need deep grammatical understanding to be correctly expanded.</description>
    <optionList>
      <options>
        <optionId>68</optionId>
        <featureId>51</featureId>
        <text>Abbreviations were not marked</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>67</optionId>
        <featureId>51</featureId>
        <text>Abbreviations were marked, but not explanded</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>399</optionId>
        <featureId>51</featureId>
        <text>Abbreviations were marked and expanded</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
  <edFeature>
    <featureId>52</featureId>
    <title>Blackening</title>
    <description>Sensible text can be marked as "blackened" and can be suppressed when exporting the text and the images </description>
    <optionList>
      <options>
        <optionId>70</optionId>
        <featureId>52</featureId>
        <text>Blackeing was not applied</text>
        <selected>false</selected>
      </options>
      <options>
        <optionId>69</optionId>
        <featureId>52</featureId>
        <text>Blackening was applied to names of persons and companies</text>
        <selected>false</selected>
      </options>
    </optionList>
  </edFeature>
</edFeatures>
  """