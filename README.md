# vuln-crawler
Web Crawler specified for snyk vulnerabilities database.

### HOW TO RUN?
Follow instruction in [google colab note](https://colab.research.google.com/drive/1nv_0hi6ySOT5KCrvj0zH_fVo_4dN-vat?usp=sharing).

### DATA BREAKDOWN: 
[an example of cleaned data](https://jsonblob.com/1198419017756172288)
* CVSS - or Common Vulnerability Scoring System: A way to evaluate and rank vulnerabilities. CVSS generates a score from 0 to 10 based on the severity of the vulnerability.
  * Base Score:
      CVSS values have been grouped into rankings as follow:
    
      | CVSS Base Score | CVSS Severity Level | 
      | -------- | -------- | 
      | 0    | None     |
      | 0.1 - 3.9    | Low     |
      | 4.0 - 6.9    | Medium     |
      | 7.0 - 8.9    | High     |
      | 9.0 - 10.0    | Critical     |
  * Attack Vector:
    The attack vector has 4 different values that can be assigned to it:
    * Network,
    * Adjacent,
    * Local,
    * Physical.
    
    Think of these as how the attacker can access the system in system in question. Ranging from _anywhere_ to _I need to physically connect something to the system_. A network value here will generate the highest CVSS value.
  * Attack Complexity: How hard is it to exploit the vulnerability:
    * Low,
    * High
  * Privileges Required: What privilesges attacker needs to have **before** exploiting the vulnerability.
    * None,
    * Low,
    * High.
    * 
    None is no access to any settings or files on the system. Low is basic user capabilities. High is administrative level privileges are needed.
  * User Interaction: How a user needs to be engaged somehow to successfully exploit the vulnerability.
    * None,
    * Required.

    When no user is required the impact on the CVSS score is highest.
  * Scope: Here it is trying to measure if the vulnerability can impact items that are outside of the security authority of the affected component. A security authority is something that controls access to objects under its control. Examples of a security authority could be an application (controls how things work inside the application), an operating system (controls how things work within the environment). Values here are:
    * Unchanged,
    * Changed.

  A scope change has the largest impact.
  * Confidentiality: the potential for unauthorized access to sensitive information:
    * High,
    * Low,
    * None.

    The greatest impact comes from the High value, or total confidentially being lost.
  * Integrity: the potential for unauthorized modification, a data breach or deletion of data:
    * High,
    * Low,
    * None.
  * Availability: the potential for denial of access to authorized users. This could be the denial access to a service or processor cycles.
    * High,
    * Low,
    * None.
* epssDetails - Exploit Prediction Scoring System:


  EPSS estimates the likelihood of a vulnerability being exploited, assigning it a probability score between 0% and 100%. The higher the score, the more likely the vulnerability will be exploited in the wild within a time period of the next 30 days. EPSS also places that score in context by producing a percentile, which is the proportion of vulnerabilities that are scored at or less than the vulnerability which therefore also indicates the level of threat the vulnerability poses.
* ExploitMaturity:
  Refers to the practicality of a vulnerability in the real world. It measures how feasible it is to exploit a vulnerability based on the following factors:
  * Whether the exploit has been published (is it “in the wild”?), and;
  * The actual “helpfulness” of those published exploits—meaning, whether the vulnerability really can be   taken advantage of more easily due to those publications.
		
  There are 3 values can be assigned to this:
  * Mature: Snyk has a published code exploit for this vulnerability.
  * Proof of Concept: Snyk has a proof-of-concept or detailed explanation of how to exploit this vulnerability.
  * No Known Exploit: Snyk did not find a proof-of-concept or a published exploit for this vulnerability.
* socialTrendAlert:
  When a specific vulnerability is gaining a lot of interest in social — Twitter, for instance — it means a lot of people are aware of the problem. Statistically, this also means more people that want to do you harm. Therefore, it can be important to put some extra focus on the vulnerabilities in your system that are socially trending.
* disclosureTime:
  This refers to the date and time when the maintainer or source of the vulnerability first published the vulnerability. For example, when a source provides Snyk with the date and time they first published a specific vulnerability, that would become the disclosed date.
* publicationTime:
  This refers to the date and time when Snyk itself published the specific vulnerability.
* commitTime:
  This refers to the date and time when a fix is published by the maintainer.
