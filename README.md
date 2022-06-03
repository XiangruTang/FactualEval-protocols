# Investigating Crowdsourcing Protocols for Evaluating the Factual Consistency of Summaries

This repository contains code, data, and templates for crowdsourcing protocols, described by the paper: [Investigating Crowdsourcing Protocols for Evaluating the Factual Consistency of Summaries](https://arxiv.org/abs/2109.09195).

## Scripts
calculate.ipynb: to calculate the score distribution, krippendorff reliability, and SHR reliability.

## Data

We released our evaluation templates and annotations to promote future work on factual consistency evaluation. The annotations can be found in [for CNN&DM data](https://drive.google.com/file/d/17d8-CkgCariNGyfftMwW0klV8kFY7xRf/view?usp=sharing), [for XSUM data](https://drive.google.com/file/d/1PiWmNE4rmisBfYNjzv36viMnxN9RVKle/view?usp=sharing) and [templates](https://drive.google.com/file/d/1i_Qq_kPFRWhh1DTu2KxEwBV_fBtPHd1W/view?usp=sharing)

## Model

The code for BART, ProphetNet, PEGASUS, and BERTSUM is based on Fairseq(-py). Our pretrained models can be found in [for CNN&DM data](https://drive.google.com/file/d/1S4xNrtykxkNfoEo4V_RJX6fvbRkpr_KB/view?usp=sharing) and [for XSUM data]()

## Citation
If you use our code in your research, please cite our work:
```bibtex
@inproceedings{tang2022investigating,
   title={Investigating Crowdsourcing Protocols for Evaluating the Factual Consistency of Summaries},
   author={Tang, Xiangru and Fabbri, Alexander R and Mao, Ziming and Adams, Griffin and Wang, Borui and Li, Haoran and Mehdad, Yashar and Radev, Dragomir},
   booktitle={North American Association for Computational Linguistics (NAACL)},
   year={2022}
}
```

